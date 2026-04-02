# services/database.py
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

# Try different import methods for compatibility
try:
    from supabase import create_client, Client
except ImportError:
    from supabase.client import Client, create_client

class DatabaseService:
    def __init__(self, supabase_url: str, supabase_key: str):
        try:
            self.client: Client = create_client(supabase_url, supabase_key)
        except TypeError:
            # Fallback for older versions
            from supabase import Client as SupabaseClient
            self.client = SupabaseClient(supabase_url, supabase_key)
        self._city_cache = {}  # Cache for city name -> ID mappings
    
    def get_cities(self) -> List[Dict]:
        """Get all cities from database"""
        try:
            response = self.client.table('cities').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Error getting cities: {e}")
            return []
    
    def get_city_id(self, city_name: str) -> Optional[int]:
        """Get city ID by name"""
        if city_name in self._city_cache:
            return self._city_cache[city_name]
            
        try:
            print(f"\n=== DEBUG: Looking up city_id for '{city_name}' ===")
            response = self.client.table('cities').select('id,name').eq('name', city_name).execute()
            print(f"City lookup response: {response.data}")
            if response.data:
                city_id = response.data[0]['id']
                print(f"Found city_id: {city_id} for '{response.data[0]['name']}'")
                self._city_cache[city_name] = city_id
                return city_id
            print(f"No city found with name '{city_name}'")
            return None
        except Exception as e:
            print(f"Error getting city ID: {e}")
            return None
    
    def upsert_kebab_place(self, google_place_id: str, name: str, address: str, 
                          city_id: int, latitude: float, longitude: float, photo_url: Optional[str] = None) -> int:
        """Insert or update a kebab place"""
        try:
            # Check if place exists
            existing = self.client.table('kebab_places').select('id').eq('google_place_id', google_place_id).execute()
            
            if existing.data:
                # Update existing
                place_id = existing.data[0]['id']
                
                # CRITICAL: Check for and fix any NULL place_id ratings for this place
                print(f"🔍 DEBUG: Upserting place {name} with place_id {place_id}")
                
                # Check if this place has any NULL place_id ratings
                # Use two-step query since ratings_history doesn't have google_place_id
                null_ratings_response = self.client.table('ratings_history').select('id').eq('kebab_place_id', place_id).is_('kebab_place_id', 'null').execute()
                
                if null_ratings_response.data:
                    print(f"⚠️  Found {len(null_ratings_response.data)} NULL place_id ratings for {name}. Fixing them...")
                    # Fix existing NULL ratings
                    for rating in null_ratings_response.data:
                        self.client.table('ratings_history').update({
                            'kebab_place_id': place_id
                        }).eq('id', rating['id']).execute()
                    print(f"✅ Fixed {len(null_ratings_response.data)} NULL place_id ratings for {name}")
                
                self.client.table('kebab_places').update({
                    'name': name,
                    'address': address,
                    'city_id': city_id,
                    'latitude': latitude,
                    'longitude': longitude,
                    'photo_url': photo_url,
                    'updated_at': datetime.now().isoformat()
                }).eq('id', place_id).execute()
                return place_id
            else:
                # Insert new
                response = self.client.table('kebab_places').insert({
                    'google_place_id': google_place_id,
                    'name': name,
                    'address': address,
                    'city_id': city_id,
                    'latitude': latitude,
                    'longitude': longitude,
                    'photo_url': photo_url
                }).execute()
                return response.data[0]['id']
        except Exception as e:
            print(f"Error upserting kebab place: {e}")
            raise
    
    def insert_rating_history(self, kebab_place_id: int, rating: float, total_reviews: int,
                            positive_percentage: float, rank_score: float, city_rank: int, 
                            update_batch_timestamp: Optional[str] = None):
        """Insert a new rating history record"""
        try:
            timestamp = datetime.now().isoformat()
            print(f"Inserting rating history for place {kebab_place_id} at {timestamp}")
            
            record_to_insert = {
                'kebab_place_id': kebab_place_id,
                'rating': rating,
                'total_reviews': total_reviews,
                'positive_percentage': positive_percentage,
                'rank_score': rank_score,
                'city_rank': city_rank,
                'data_fetched_at': timestamp
            }
           
            record_to_insert['update_batch_timestamp'] = update_batch_timestamp or timestamp
            
            print(f"DEBUG: Record to insert into ratings_history: {record_to_insert}")
            response = self.client.table('ratings_history').insert(record_to_insert).execute()
            
            print(f"DEBUG: Supabase response for ratings_history: {response}")
            print(f"Successfully inserted rating history: {response.data}")
            return response
        except Exception as e:
            print(f"Error inserting rating history: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def get_last_update_time(self, city_name: str) -> Optional[datetime]:
        """Get the last update time for a city"""
        try:
            # Complex query with joins
            response = self.client.rpc('get_city_last_update', {'city_name': city_name}).execute()
            if response.data:
                return datetime.fromisoformat(response.data[0]['max_date'])
            return None
        except:
            # Fallback to simpler query
            try:
                city_id = self.get_city_id(city_name)
                if not city_id:
                    return None
                
                response = self.client.table('ratings_history').select('data_fetched_at').order('data_fetched_at', desc=True).limit(1).execute()
                if response.data:
                    return datetime.fromisoformat(response.data[0]['data_fetched_at'])
                return None
            except Exception as e:
                print(f"Error getting last update time: {e}")
                return None
    
    def get_city_rankings(self, city_name: str, limit: int = 10, offset: int = 0) -> List[Dict]:
        try:
            print(f"\n=== DEBUG: Getting rankings for '{city_name}' ===")
            city_id = self.get_city_id(city_name)
            if not city_id:
                print(f"No city_id found for '{city_name}'")
                return []

            # Try RPC function first, fallback to optimized query if not available
            try:
                response = self.client.rpc('get_city_rankings_with_latest_ratings_v4', {
                    'p_city_id': city_id,
                    'p_limit': limit,
                    'p_offset': offset
                }).execute()
                
                if response.data:
                    rankings = response.data
                    # Add coordinates to RPC response data using bulk fetch
                    print("RPC function succeeded, adding coordinates to response via bulk fetch...")
                    
                    google_ids = [k['google_place_id'] for k in rankings]
                    places_response = self.client.table('kebab_places').select(
                        'google_place_id, latitude, longitude, photo_url'
                    ).in_('google_place_id', google_ids).execute()
                    
                    place_map = {p['google_place_id']: p for p in places_response.data}
                    
                    for kebab in rankings:
                        place_data = place_map.get(kebab['google_place_id'], {})
                        kebab['latitude'] = place_data.get('latitude')
                        kebab['longitude'] = place_data.get('longitude')
                        kebab['photo_url'] = place_data.get('photo_url')
                            
                else:
                    raise Exception("No data from RPC")
                    
            except Exception as e:
                print(f"RPC function failed, falling back to optimized query: {e}")
                
                # Fallback query - include latitude and longitude
                response = self.client.table('kebab_places').select(
                    '''
                    id,
                    name,
                    address,
                    google_place_id,
                    latitude,
                    longitude,
                    photo_url,
                    ratings_history!inner(
                        rating,
                        total_reviews,
                        positive_percentage,
                        rank_score,
                        city_rank,
                        data_fetched_at
                    )
                    '''
                ).eq('city_id', city_id).execute()
                
                if not response.data:
                    return []
                
                # Process response to get latest rating per place
                latest_ratings = {}
                for place in response.data:
                    if place.get('ratings_history'):
                        # Get most recent rating
                        latest_rating = max(place['ratings_history'], 
                                        key=lambda x: x['data_fetched_at'])
                        latest_ratings[place['id']] = {
                            'id': place['id'],
                            'name': place['name'],
                            'address': place['address'],
                            'google_place_id': place['google_place_id'],
                            'latitude': place.get('latitude'),
                            'longitude': place.get('longitude'),
                            'photo_url': place.get('photo_url'),
                            'rating': latest_rating['rating'],
                            'total_reviews': latest_rating['total_reviews'],
                            'positive_percentage': latest_rating['positive_percentage'],
                            'rank_score': latest_rating['rank_score'],
                            'city_rank': latest_rating['city_rank'],
                            'data_fetched_at': latest_rating['data_fetched_at']
                        }
                
                rankings = list(latest_ratings.values())
            
            # Sort by rank_score descending
            rankings = sorted(rankings, key=lambda x: (x['rank_score'], x['total_reviews']), reverse=True)
            
            # Ensure sequential city_rank
            for i, kebab in enumerate(rankings):
                kebab['city_rank'] = i + 1
            
            # Get previous rankings
            print("Getting previous rankings...")
            previous_rankings = self.get_previous_rankings(city_name)
            print(f"Found {len(previous_rankings)} previous rankings")
            
            # Create a map for quick lookup
            previous_rank_map = {r['google_place_id']: r['city_rank'] for r in previous_rankings}
            
            # Add rank change data to each kebab
            for kebab in rankings:
                google_place_id = kebab['google_place_id']
                
                if google_place_id in previous_rank_map:
                    previous_rank = previous_rank_map[google_place_id]
                    current_rank = kebab['city_rank']
                    rank_change = previous_rank - current_rank
                    
                    kebab['rank_change'] = rank_change
                    kebab['is_new'] = False
                    
                    # Add rank change indicator for the UI
                    if rank_change > 0:
                        kebab['rank_change_indicator'] = 'up'
                    elif rank_change < 0:
                        kebab['rank_change_indicator'] = 'down'
                    else:
                        kebab['rank_change_indicator'] = 'neutral'
                    
                    print(f"  {kebab['name']}: Rank {previous_rank} → {current_rank} (Change: {rank_change})")
                else:
                    # Check if this is a truly new kebab or an expired NEW badge
                    # Get the first seen date for this kebab
                    try:
                        place_response = self.client.table('kebab_places').select(
                            'created_at'
                        ).eq('google_place_id', google_place_id).execute()
                        
                        if place_response.data and place_response.data[0].get('created_at'):
                            first_seen = datetime.fromisoformat(place_response.data[0]['created_at'])
                            days_since_first_seen = (datetime.now() - first_seen).days
                            
                            # If kebab is older than 7 days, don't show as NEW
                            if days_since_first_seen > 7:
                                kebab['rank_change'] = 0
                                kebab['is_new'] = False
                                kebab['rank_change_indicator'] = 'neutral'
                                print(f"  {kebab['name']}: NEUTRAL (NEW badge expired after {days_since_first_seen} days)")
                            else:
                                # Truly new kebab (less than 7 days old)
                                kebab['rank_change'] = None
                                kebab['is_new'] = True
                                kebab['rank_change_indicator'] = 'new'
                                print(f"  {kebab['name']}: NEW entry ({days_since_first_seen} days old)")
                        else:
                            # Fallback - no created_at date, treat as new
                            kebab['rank_change'] = None
                            kebab['is_new'] = True
                            kebab['rank_change_indicator'] = 'new'
                            print(f"  {kebab['name']}: NEW entry (no creation date)")
                            
                    except Exception as e:
                        # If we can't get the creation date, treat as new
                        print(f"  Warning: Could not get creation date for {kebab['name']}: {e}")
                        kebab['rank_change'] = None
                        kebab['is_new'] = True
                        kebab['rank_change_indicator'] = 'new'
                        print(f"  {kebab['name']}: NEW entry (error getting date)")
            
            # Return only requested number
            return rankings[:limit]
            
        except Exception as e:
            print(f"Error getting city rankings: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_global_rankings(self, limit: int = 10) -> List[Dict]:
        """Get global top rankings"""
        try:
            # Get all recent kebab places with their latest ratings - include coordinates
            response = self.client.table('kebab_places').select(
                'id, name, address, google_place_id, latitude, longitude, photo_url, cities!inner(name), ratings_history!inner(*)'
            ).execute()
            
            # Get latest rating for each place
            latest_ratings = {}
            for place in response.data:
                place_id = place['id']
                # Get the most recent rating
                if place['ratings_history']:
                    ratings = sorted(place['ratings_history'], 
                                   key=lambda x: x['data_fetched_at'], 
                                   reverse=True)
                    if ratings:
                        latest_rating = ratings[0]
                        latest_ratings[place_id] = {
                            'id': place_id,
                            'name': place['name'],
                            'address': place['address'],
                            'city': place['cities']['name'],
                            'google_place_id': place['google_place_id'],
                            'latitude': place.get('latitude'),
                            'longitude': place.get('longitude'),
                            'photo_url': place.get('photo_url'),
                            'rating': latest_rating['rating'],
                            'total_reviews': latest_rating['total_reviews'],
                            'positive_percentage': latest_rating['positive_percentage'],
                            'rank_score': latest_rating['rank_score']
                        }
            
            # Sort by rank_score descending, then by total_reviews descending
            sorted_kebabs = sorted(latest_ratings.values(), 
                                 key=lambda x: (x['rank_score'], x['total_reviews']), 
                                 reverse=True)
            
            # Add global rank
            for i, kebab in enumerate(sorted_kebabs[:limit]):
                kebab['global_rank'] = i + 1
            
            return sorted_kebabs[:limit]
            
        except Exception as e:
            print(f"Error getting global rankings: {e}")
            return []
    
    def get_all_recent_ratings(self) -> List[Dict]:
        """Get all recent ratings for global ranking calculation"""
        try:
            # Get the most recent rating for each kebab place
            response = self.client.table('ratings_history').select(
                '*, kebab_places!inner(name, google_place_id)'
            ).order('data_fetched_at', desc=True).execute()
            
            # Deduplicate to get only the latest for each place
            latest_ratings = {}
            for rating in response.data:
                place_id = rating['kebab_place_id']
                if place_id not in latest_ratings:
                    latest_ratings[place_id] = {
                        'rating_id': rating['id'],
                        'place_id': rating['kebab_places']['google_place_id'],
                        'google_place_id': rating['kebab_places']['google_place_id'],
                        'name': rating['kebab_places']['name'],
                        'rating': rating['rating'],
                        'total_reviews': rating['total_reviews'],
                        'positive_percentage': rating['positive_percentage'],
                        'rank_score': rating['rank_score']
                    }
            
            return list(latest_ratings.values())
            
        except Exception as e:
            print(f"Error getting all recent ratings: {e}")
            return []
    
    def get_previous_rankings(self, city_name: str) -> List[Dict]:
        """Get rankings from the previous full update cycle using batch timestamps."""
        try:
            city_id = self.get_city_id(city_name)
            if not city_id:
                return []

            print(f"\n=== DEBUG: Getting previous rankings for '{city_name}' using batch logic ===")

            # Step 1: Identify the "current" batch timestamp.
            # We get the single most recent rating record for the city and check its batch timestamp.
            # This requires a join, which is best done with an RPC. For now, a two-step query.
            
            # Get the most recent rating_history ID for the city to find its batch timestamp
            latest_rating_response = self.client.table('ratings_history').select(
                'id, update_batch_timestamp, kebab_places!inner(city_id)'
            ).eq('kebab_places.city_id', city_id).order(
                'data_fetched_at', desc=True
            ).limit(1).execute()

            if not latest_rating_response.data:
                print("No ratings history found for this city. Cannot determine previous rankings.")
                return []

            current_batch_timestamp = latest_rating_response.data[0].get('update_batch_timestamp')
            print(f"Current batch timestamp identified as: {current_batch_timestamp}")

            if not current_batch_timestamp:
                print("Latest rating record has no 'update_batch_timestamp'. Falling back to old logic or returning empty.")
                # Fallback to old logic or return empty if new system is expected
                # For now, let's assume if there's no batch timestamp, we can't determine previous.
                return []

            # Step 2: Identify the "previous" batch timestamp.
            # This is the most recent batch timestamp that is strictly less than the current one.
            # This is highly recommended to be an RPC for efficiency and correctness.
            # RPC: get_previous_batch_timestamp(p_city_id INT, p_current_batch_timestamp TEXT)
            
            # --- Conceptual RPC call ---
            # previous_batch_timestamp_rpc_response = self.client.rpc('get_previous_batch_timestamp', {
            #     'p_city_id': city_id,
            #     'p_current_batch_timestamp': current_batch_timestamp
            # }).execute()
            # if previous_batch_timestamp_rpc_response.data:
            #     previous_batch_timestamp = previous_batch_timestamp_rpc_response.data[0].get('timestamp')
            # else:
            #     print("No previous batch timestamp found via RPC.")
            #     return []
            # --- End of conceptual RPC call ---

            # --- Fallback logic if RPC is not yet implemented (less efficient) ---
            # This is a simplified approach and might not be performant on large datasets.
            print("Attempting to find previous batch timestamp via fallback query...")
            
            # Get all distinct batch timestamps for the city, ordered descending
            # First get the kebab places for this city
            kebab_places_response = self.client.table('kebab_places').select(
                'id'
            ).eq('city_id', city_id).execute()
            
            if not kebab_places_response.data:
                print("No kebab places found for this city.")
                return []
            
            kebab_place_ids = [kp['id'] for kp in kebab_places_response.data]
            
            # Now get batch timestamps for these specific places
            all_batches_response = self.client.table('ratings_history').select(
                'update_batch_timestamp'
            ).in_('kebab_place_id', kebab_place_ids).not_.is_('update_batch_timestamp', 'null').execute()
            
            if not all_batches_response.data:
                print("No batch timestamps found at all.")
                return []

            # Extract unique timestamps and sort
            unique_batch_timestamps = sorted(list(set(
                r['update_batch_timestamp'] for r in all_batches_response.data if r['update_batch_timestamp']
            )), reverse=True)

            print(f"Found {len(unique_batch_timestamps)} unique batch timestamps. Latest 5: {unique_batch_timestamps[:5]}")

            if len(unique_batch_timestamps) < 2 or unique_batch_timestamps[0] != current_batch_timestamp:
                print(f"Not enough distinct batch cycles ({len(unique_batch_timestamps)} found) or current batch is not the latest. Cannot determine previous rankings.")
                print("This is normal for the first update - all kebabs will be marked as NEW.")
                return []
            
            previous_batch_timestamp = unique_batch_timestamps[1]
            print(f"Previous batch timestamp identified as: {previous_batch_timestamp}")
            # --- End of fallback logic ---

            if not previous_batch_timestamp:
                print("Could not determine the previous batch timestamp. All kebabs might be new.")
                return []

            # Step 3: Fetch all rankings for that specific previous_batch_timestamp.
            # This also is best done with an RPC.
            # RPC: get_rankings_for_batch(p_city_id INT, p_batch_timestamp TEXT)

            # --- Conceptual RPC call ---
            # previous_rankings_response = self.client.rpc('get_rankings_for_batch', {
            #     'p_city_id': city_id,
            #     'p_batch_timestamp': previous_batch_timestamp
            # }).execute()
            # if previous_rankings_response.data:
            #     return [{
            #         'google_place_id': r['google_place_id'],
            #         'city_rank': r['city_rank'],
            #         'data_fetched_at': r['data_fetched_at'],
            #         'is_approximate': False
            #     } for r in previous_rankings_response.data]
            # else:
            #     return []
            # --- End of conceptual RPC call ---

            # --- Fallback logic if RPC is not yet implemented ---
            print(f"Fetching rankings for previous batch: {previous_batch_timestamp}")
            
            # First get the ratings_history records for the previous batch
            ratings_data = self.client.table('ratings_history').select(
                'kebab_place_id, city_rank, data_fetched_at'
            ).eq('update_batch_timestamp', previous_batch_timestamp).execute()
            
            if not ratings_data.data:
                print(f"No ranking data found for previous batch timestamp: {previous_batch_timestamp}")
                return []
            
            # Get the place IDs from the ratings data
            kebab_place_ids = [r['kebab_place_id'] for r in ratings_data.data]
            
            # Now get the google_place_ids for these places
            places_data = self.client.table('kebab_places').select(
                'id, google_place_id'
            ).in_('id', kebab_place_ids).execute()
            
            # Create a mapping from place_id to google_place_id
            place_id_to_google_id = {p['id']: p['google_place_id'] for p in places_data.data}
            
            # Combine the data
            formatted_previous_rankings = []
            for rating in ratings_data.data:
                google_place_id = place_id_to_google_id.get(rating['kebab_place_id'])
                if google_place_id and rating.get('city_rank') is not None:
                    formatted_previous_rankings.append({
                        'google_place_id': google_place_id,
                        'city_rank': rating['city_rank'],
                        'data_fetched_at': rating['data_fetched_at'],
                        'is_approximate': False
                    })

            if not formatted_previous_rankings:
                print(f"No ranking data found for previous batch timestamp: {previous_batch_timestamp}")
                return []
            # --- End of fallback logic ---
            
            print(f"Found {len(formatted_previous_rankings)} previous rankings from batch {previous_batch_timestamp}")
            return formatted_previous_rankings

        except Exception as e:
            print(f"Error getting previous rankings with batch logic: {e}")
            import traceback
            traceback.print_exc()
            return []
    def get_most_recent_update(self) -> Optional[datetime]:
        """Get the most recent update time across all cities"""
        try:
            print("\n=== DEBUG: Querying ratings_history for most recent timestamp ===")
            response = self.client.table('ratings_history').select('data_fetched_at').order('data_fetched_at', desc=True).execute()
            print(f"Full response: {response}")
            print(f"Response data type: {type(response.data)}")
            print(f"Found {len(response.data)} records in ratings_history")
            
            if not response.data:
                print("No records found in ratings_history table")
                return None
                
            first_record = response.data[0]
            print(f"First record type: {type(first_record)}")
            print(f"First record contents: {first_record}")
            
            timestamp_str = first_record['data_fetched_at']
            print(f"Raw timestamp from DB: {timestamp_str} (type: {type(timestamp_str)})")
            
            try:
                # Parse timestamp
                if isinstance(timestamp_str, str):
                    print("Timestamp is a string, attempting to parse")
                    
                    # Clean up timestamp format
                    if timestamp_str.endswith('Z'):
                        timestamp_str = timestamp_str[:-1] + '+00:00'
                    elif '+' not in timestamp_str and 'Z' not in timestamp_str:
                        # Handle microseconds issue
                        if '.' in timestamp_str and 'T' in timestamp_str:
                            date_part, time_part = timestamp_str.split('T')
                            if '.' in time_part:
                                time_main, microseconds = time_part.split('.')
                                # Ensure exactly 6 digits for microseconds
                                microseconds = microseconds[:6].ljust(6, '0')
                                timestamp_str = f"{date_part}T{time_main}.{microseconds}+00:00"
                            else:
                                timestamp_str += '+00:00'
                        else:
                            timestamp_str += '+00:00'
                    
                    try:
                        parsed = datetime.fromisoformat(timestamp_str)
                        print(f"Successfully parsed timestamp: {parsed}")
                        return parsed
                    except ValueError as e:
                        print(f"fromisoformat failed: {e}")
                        # Fallback parsing
                        from dateutil import parser
                        parsed = parser.parse(timestamp_str)
                        return parsed
                else:
                    print(f"Unexpected timestamp type: {type(timestamp_str)}")
                    return None
            except Exception as parse_error:
                print(f"Failed to parse timestamp: {parse_error}")
                import traceback
                traceback.print_exc()
                return None
        except Exception as e:
            print(f"Error getting most recent update: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def update_global_rank(self, rating_id: int, global_rank: int):
        """Update global rank for a rating"""
        try:
            self.client.table('ratings_history').update({
                'global_rank': global_rank
            }).eq('id', rating_id).execute()
        except Exception as e:
            print(f"Error updating global rank: {e}")
    
    def get_last_two_batches(self) -> List[str]:
        """Get the two most recent 'Update Cycles' by grouping unique timestamps."""
        try:
            # Get all unique batch timestamps
            response = self.client.table('ratings_history') \
                .select('update_batch_timestamp') \
                .order('update_batch_timestamp', desc=True) \
                .execute()
            
            if not response.data:
                return []

            all_hits = []
            seen = set()
            for r in response.data:
                ts = r.get('update_batch_timestamp')
                if ts and ts not in seen:
                    all_hits.append(ts)
                    seen.add(ts)
            
            if not all_hits:
                return []

            # Grouping Logic: Treat any timestamps within 6 hours as the same "Batch Cycle"
            # We want the most recent cycle, and the cycle before that.
            cycles = []
            if all_hits:
                current_cycle_representatives = []
                last_ts_obj = None
                
                for ts_str in all_hits:
                    # Robust parsing for various ISO-like formats from Postgres
                    try:
                        # Replace space with T for isoformat consistency
                        clean_ts = ts_str.replace(' ', 'T')
                        # fromisoformat handles +00:00 correctly in modern Python
                        ts_obj = datetime.fromisoformat(clean_ts)
                    except ValueError:
                        try:
                            # Fallback: remove timezone manually if it still fails
                            if '+' in ts_str:
                                clean_ts = ts_str.split('+')[0].replace(' ', 'T')
                                ts_obj = datetime.fromisoformat(clean_ts)
                            else:
                                continue
                        except Exception:
                            continue
                        
                    if last_ts_obj is None:
                        # First timestamp defines the start of the most recent cycle
                        current_cycle_representatives.append(ts_str)
                        last_ts_obj = ts_obj
                    else:
                        # If this timestamp is more than 6 hours away from the previous one, it's a new cycle
                        diff = (last_ts_obj - ts_obj).total_seconds() / 3600
                        if diff > 6:
                            # Start a new cycle
                            cycles.append(current_cycle_representatives)
                            current_cycle_representatives = [ts_str]
                            last_ts_obj = ts_obj
                            if len(cycles) >= 2:
                                break
                        else:
                            # Part of the same cycle
                            current_cycle_representatives.append(ts_str)
                            # We don't update last_ts_obj here to keep the relative diff consistent across the window
                
                # Add the last pending cycle if we didn't hit the break
                if current_cycle_representatives and len(cycles) < 2:
                    cycles.append(current_cycle_representatives)

            # Return the first representative of each of the last two cycles
            # The report script will need to be updated to handle MULTIPLE timestamps per cycle
            # but for now, we'll return the list of timestamps for the last two cycles
            return cycles
        except Exception as e:
            print(f"Error identifying update cycles: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_rankings_by_batch(self, batch_timestamp_or_list) -> List[Dict]:
        """Get rankings for a specific batch timestamp or a list of timestamps (a cycle)."""
        try:
            query = self.client.table('ratings_history').select(
                '*, kebab_places!inner(name, google_place_id, cities!inner(name))'
            )
            
            if isinstance(batch_timestamp_or_list, list):
                # Use .in_ filters for multiple timestamps in a cycle
                query = query.in_('update_batch_timestamp', batch_timestamp_or_list)
            else:
                query = query.eq('update_batch_timestamp', batch_timestamp_or_list)
                
            response = query.execute()
            
            rankings = []
            for r in response.data:
                rankings.append({
                    'place_id': r['kebab_place_id'],
                    'google_place_id': r['kebab_places']['google_place_id'],
                    'name': r['kebab_places']['name'],
                    'city': r['kebab_places']['cities']['name'],
                    'rating': r['rating'],
                    'total_reviews': r['total_reviews'],
                    'rank_score': r['rank_score'],
                    'city_rank': r['city_rank'],
                    'global_rank': r.get('global_rank')
                })
            return rankings
        except Exception as e:
            print(f"Error getting rankings by batch: {e}")
            return []
    
    def recalculate_city_rankings(self, city_id: int):
        """Recalculate rankings for all kebabs in a city"""
        try:
            # Get all kebab places in the city with their latest ratings
            response = self.client.table('kebab_places').select(
                'id, ratings_history!inner(*)'
            ).eq('city_id', city_id).execute()
            
            # Get latest ratings for each place
            latest_ratings = []
            for place in response.data:
                if place['ratings_history']:
                    sorted_ratings = sorted(place['ratings_history'], 
                                          key=lambda x: x['data_fetched_at'], 
                                          reverse=True)
                    if sorted_ratings:
                        latest_rating = sorted_ratings[0]
                        latest_rating['place_id'] = place['id']
                        latest_ratings.append(latest_rating)
            
            # Sort by rank_score and assign new city_rank
            sorted_ratings = sorted(latest_ratings, 
                                  key=lambda x: (x['rank_score'], x['total_reviews']), 
                                  reverse=True)
            
            # Update city_rank in the database
            for i, rating in enumerate(sorted_ratings):
                self.client.table('ratings_history').update({
                    'city_rank': i + 1
                }).eq('id', rating['id']).execute()
                
        except Exception as e:
            print(f"Error recalculating city rankings: {e}")
