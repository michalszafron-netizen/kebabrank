from pocketbase import PocketBase
from datetime import datetime, timezone
from typing import List, Dict, Optional
import os
import requests
import tempfile
import time
from pocketbase.errors import ClientResponseError

class PocketbaseService:
    def __init__(self, pb_url: str, pb_email: str = None, pb_password: str = None):
        self.url = pb_url
        self.client = PocketBase(pb_url)
        self.email = pb_email or os.getenv('PB_EMAIL')
        self.password = pb_password or os.getenv('PB_PASSWORD')
        self._is_authed = False
        self._last_auth_time = 0
        self._auth_retry_count = 0
        self._city_cache = {}
        self._max_auth_retries = 3
        self._auth_retry_delay = 5  # seconds

    def _ensure_auth(self, force_refresh=False):
        """Ensure we have a valid authentication token with automatic refresh"""
        # If we're already authenticated and not forcing refresh, check if token is still valid
        if self._is_authed and not force_refresh:
            # Check if token is likely expired (more than 12 hours old)
            if time.time() - self._last_auth_time < 12 * 3600:  # 12 hours
                return True
        
        # If no credentials, we can't authenticate
        if not self.email or not self.password:
            print("Pocketbase Auth Error: Missing email or password credentials")
            return False
        
        # Try to authenticate with retry logic
        for attempt in range(self._max_auth_retries):
            try:
                print(f"Authenticating with PocketBase (attempt {attempt + 1}/{self._max_auth_retries})...")
                self.client.admins.auth_with_password(self.email, self.password)
                self._is_authed = True
                self._last_auth_time = time.time()
                self._auth_retry_count = 0
                print("PocketBase authentication successful")
                return True
            except Exception as e:
                print(f"Pocketbase Auth Error (attempt {attempt + 1}): {e}")
                self._is_authed = False
                
                # If this is the last attempt, give up
                if attempt == self._max_auth_retries - 1:
                    print(f"Failed to authenticate with PocketBase after {self._max_auth_retries} attempts")
                    return False
                
                # Wait before retrying
                time.sleep(self._auth_retry_delay * (attempt + 1))  # Exponential backoff
        
        return False

    def _handle_auth_error(self, e: Exception):
        """Handle authentication errors and attempt to re-authenticate"""
        # Check if this is an authentication error (403)
        if isinstance(e, ClientResponseError) and e.status == 403:
            print("Authentication error detected (403), attempting to re-authenticate...")
            self._is_authed = False
            return self._ensure_auth(force_refresh=True)
        return False
    
    def _execute_with_auth_retry(self, func, *args, **kwargs):
        """Execute a function with authentication retry logic"""
        max_retries = 2
        for attempt in range(max_retries + 1):  # +1 for the initial attempt
            try:
                # Ensure we're authenticated before each attempt
                if not self._ensure_auth():
                    print(f"Authentication failed, cannot execute function")
                    return None
                
                # Execute the function
                return func(*args, **kwargs)
                
            except ClientResponseError as e:
                if e.status == 403 and attempt < max_retries:
                    print(f"Authentication error (403) on attempt {attempt + 1}, re-authenticating...")
                    self._is_authed = False
                    continue
                else:
                    # Re-raise if not a 403 or we've exhausted retries
                    raise
            except Exception as e:
                # Re-raise other exceptions
                raise
        
        return None

    def get_cities(self) -> List[Dict]:
        """Get all cities from database"""
        try:
            # Use auth retry wrapper
            def _get_cities():
                return self.client.collection('cities').get_full_list()
            
            records = self._execute_with_auth_retry(_get_cities)
            if records is None:
                return []
            return [self._format_record(r) for r in records]
        except Exception as e:
            print(f"Error getting cities: {e}")
            return []

    @staticmethod
    def _normalize_city(s: str) -> str:
        return s.lower().translate(str.maketrans('ąćęłńóśźż', 'acelnoszz'))

    def get_city_id(self, city_name: str) -> Optional[str]:
        """Get city ID by name (Pocketbase IDs are strings).
        Falls back to diacritics-insensitive match (e.g. 'Bielsko-Biala' → 'Bielsko-Biała')."""
        if city_name in self._city_cache:
            return self._city_cache[city_name]
        try:
            def _get_city_id():
                # 1. Exact match
                try:
                    record = self.client.collection('cities').get_first_list_item(f'name="{city_name}"')
                    if record:
                        self._city_cache[city_name] = record.id
                        return record.id
                except Exception:
                    pass
                # 2. Fuzzy fallback — normalize diacritics on both sides
                all_cities = self.client.collection('cities').get_full_list()
                norm_input = self._normalize_city(city_name)
                for c in all_cities:
                    if self._normalize_city(c.name) == norm_input:
                        print(f"  ✓ Matched '{city_name}' → '{c.name}'")
                        self._city_cache[city_name] = c.id
                        return c.id
                return None

            result = self._execute_with_auth_retry(_get_city_id)
            if result is None:
                print(f"Error getting city ID for {city_name}: Not found or authentication failed")
            return result
        except Exception as e:
            print(f"Error getting city ID for {city_name}: {e}")
        return None

    def get_city_rankings(self, city_name: str, limit: int = 10, offset: int = 0) -> List[Dict]:
        """Get latest rankings for a specific city by querying ratings collection directly."""
        try:
            # Use auth retry wrapper
            def _get_city_rankings():
                city_id = self.get_city_id(city_name)
                if not city_id:
                    return []

                # Fetch all ratings for this city (sorted newest first)
                records = self.client.collection('ratings').get_list(1, 500, query_params={
                    "filter": f'kebab_place.city="{city_id}"',
                    "sort": "-created",
                    "expand": "kebab_place"
                })
                
                if not records.items:
                    return []
                
                from datetime import datetime, timedelta
                latest_str = records.items[0].created
                if isinstance(latest_str, str):
                    try: latest_dt = datetime.fromisoformat(latest_str.replace('Z', '+00:00'))
                    except: latest_dt = datetime.strptime(latest_str, '%Y-%m-%d %H:%M:%S')
                else:
                    latest_dt = latest_str

                # Deduplicate to find unique kebabs in current batch
                seen_google_ids = set()
                batch_items = []
                for r in records.items:
                    p = getattr(r, "expand", {}).get("kebab_place")
                    if not p:
                        continue
                    g_id = getattr(p, 'google_place_id', '')
                    if not g_id or g_id in seen_google_ids:
                        continue
                    seen_google_ids.add(g_id)
                    batch_items.append(r)
                
                # Ghost elimination: keep only places whose most recent rating has city_rank > 0.
                # After reset_city_ranks, ghost places have city_rank=0 in their latest rating.
                # Valid places have city_rank>0 set by insert_rating_history during update.
                batch_items = [r for r in batch_items if getattr(r, 'city_rank', 0) > 0]

                # Sort by rank_score primarily to get current ranks
                batch_items.sort(key=lambda x: (getattr(x, 'rank_score', 0), getattr(x, 'total_reviews', 0)), reverse=True)
                
                # --- Trend Calculation for Cities ---
                # We need to find the rank from the PREVIOUS update session.
                # To do this, we find the oldest record in our current batch as a threshold.
                # All batch items are very recent.
                batch_by_date = sorted(batch_items, key=lambda x: x.created)
                batch_threshold = batch_by_date[0].created if batch_by_date else latest_dt
                
                # We now search for the last known rating record that had a rank > 0 
                # (to ignore those reset to zero) and was created before this batch.
                prev_records = self.client.collection('ratings').get_list(1, 1000, query_params={
                    "filter": f'kebab_place.city="{city_id}" && city_rank > 0 && created < "{batch_threshold}"',
                    "sort": "-created",
                    "expand": "kebab_place"
                })
                
                prev_rankings = {} # google_place_id -> rank
                seen_prev = set()
                prev_items = []
                
                for r in prev_records.items:
                    p = getattr(r, "expand", {}).get("kebab_place")
                    if not p: continue
                    g_id = getattr(p, 'google_place_id', '')
                    if not g_id or g_id in seen_prev: continue
                    
                    seen_prev.add(g_id)
                    prev_items.append(r)
                
                # We no longer need to sort prev_items and re-calculate relative ranks.
                # When these old records were created, the `recalculate_city_rankings` function 
                # already saved their absolute `city_rank` at that moment in time.
                for r in prev_items:
                    p = getattr(r, "expand", {}).get("kebab_place")
                    if getattr(r, 'city_rank', 0) > 0:
                        prev_rankings[p.google_place_id] = r.city_rank

                # 2. Compare Current vs Previous
                for i, r in enumerate(batch_items):
                    p = getattr(r, "expand", {}).get("kebab_place")
                    g_id = p.google_place_id
                    current_rank = i + 1
                    
                    # Store trend metadata in r itself for later formatting
                    # (Need to handle both Record objects and dicts if used)
                    trend_meta = {
                        'rank_change': 0,
                        'rank_change_indicator': 'neutral',
                        'is_new': False
                    }
                    
                    if g_id in prev_rankings:
                        old_rank = prev_rankings[g_id]
                        change = old_rank - current_rank
                        trend_meta['rank_change'] = change
                        trend_meta['rank_change_indicator'] = 'up' if change > 0 else ('down' if change < 0 else 'neutral')
                        trend_meta['is_new'] = False
                    elif prev_rankings:
                        # Only mark as NEW if it's a truly newly created record in our DB
                        from datetime import datetime, timedelta, timezone
                        try:
                            p_created = p.created if isinstance(p.created, datetime) else datetime.fromisoformat(p.created.replace('Z', '+00:00'))
                            # Make naive datetimes aware
                            if p_created.tzinfo is None:
                                p_created = p_created.replace(tzinfo=timezone.utc)
                                
                            # Use 48h window for NEW badge to be safe across different update batch times
                            trend_meta['is_new'] = p_created > (datetime.now(timezone.utc) - timedelta(hours=48))
                        except Exception as e:
                            print(f"Error checking is_new: {e}")
                            trend_meta['is_new'] = False
                        
                        if trend_meta['is_new']:
                            trend_meta['rank_change_indicator'] = 'neutral'
                            trend_meta['rank_change'] = 0

                    # Attach this to record (workaround for immutable Record objects)
                    # We'll use this in the next loop to build the final dict
                    setattr(r, '_trend_data', trend_meta)

                # Apply offset and limit
                paginated_items = batch_items[offset : offset + limit]
                
                rankings = []
                for r in paginated_items:
                    p = getattr(r, "expand", {}).get("kebab_place")
                    if not p: continue
                    
                    # Use ai_score from rating if > 0, else fallback to rank_score or whatever base has
                    base_ai_score = getattr(r, 'ai_score', 0)
                    trend = getattr(r, '_trend_data', {'rank_change': 0, 'rank_change_indicator': 'neutral', 'is_new': False})
                    
                    rankings.append({
                        'id': p.id,
                        'name': p.name,
                        'address': p.address,
                        'google_place_id': p.google_place_id,
                        'latitude': getattr(p, 'lat', 0),
                        'longitude': getattr(p, 'lng', 0),
                        'photo_url': self.get_file_url(p, getattr(p, 'photo', '')),
                        'rating': r.rating,
                        'total_reviews': r.total_reviews,
                        'rank_score': r.rank_score,
                        'city_rank': getattr(r, 'city_rank', 0),
                        'data_fetched_at': r.created,
                        'rank_change': trend['rank_change'], 
                        'rank_change_indicator': trend['rank_change_indicator'],
                        'is_new': trend['is_new'],
                        'has_ai_analysis': base_ai_score > 0,
                        'ai_score': base_ai_score if base_ai_score > 0 else r.rank_score,
                        'opening_hours': getattr(p, 'opening_hours', None),
                    })

                return rankings
            
            result = self._execute_with_auth_retry(_get_city_rankings)
            if result is None:
                return []
            return result
        except Exception as e:
            print(f"Error getting rankings for {city_name}: {e}")
            return []

    def get_global_rankings(self, limit: int = 50) -> List[Dict]:
        """Get top global kebab rankings — fast single-query approach.
        
        Finds latest timestamp, filters to a 5-minute window, grabs top 500 by score
        (one PocketBase call), then deduplicates by google_place_id.
        """
        try:
            # Use auth retry wrapper
            def _get_global_rankings():
                # Try reading from pre-computed global_top collection first
                try:
                    top_records = self.client.collection('global_top').get_list(
                        1, limit,
                        query_params={"sort": "-rank_score"}
                    )
                    if top_records.items and len(top_records.items) > 0:
                        results = []
                        for i, r in enumerate(top_records.items):
                            results.append({
                                'id': getattr(r, 'place_id', r.id),
                                'name': r.name,
                                'address': getattr(r, 'address', ''),
                                'city': getattr(r, 'city', 'Unknown'),
                                'google_place_id': getattr(r, 'google_place_id', ''),
                                'latitude': getattr(r, 'lat', 0),
                                'longitude': getattr(r, 'lng', 0),
                                'photo_url': getattr(r, 'photo_url', ''),
                                'rating': getattr(r, 'rating', 0),
                                'total_reviews': getattr(r, 'total_reviews', 0),
                                'rank_score': r.rank_score,
                                'ai_score': getattr(r, 'ai_score', r.rank_score),
                                'has_ai_analysis': getattr(r, 'has_ai_analysis', False),
                                'opening_hours': getattr(r, 'opening_hours', None),
                                'global_rank': i + 1
                            })
                        return results
                except Exception:
                    pass  # Collection doesn't exist yet, fall back to live query
                
                # Live query fallback: fast single-query approach
                from datetime import datetime, timedelta
                
                # Find the latest timestamp (kept to know if DB is totally empty)
                latest_record = self.client.collection('ratings').get_first_list_item(
                    "", query_params={"sort": "-created"}
                )
                if not latest_record:
                    return []
                
                # Step 2: Fetch recent records, sorted by -created
                # We process 500 records to find the latest top scores,
                # which is enough to cover the top list while keeping queries fast (<1s).
                records = self.client.collection('ratings').get_list(
                    1, 500,
                    query_params={
                        "sort": "-created",
                        "expand": "kebab_place,kebab_place.city"
                    }
                )
                
                if not records.items:
                    return []
                
                # Step 3: Deduplicate by google_place_id (keep FIRST = most recent)
                seen_ids = set()
                unique_items = []
                
                for r in records.items:
                    p = getattr(r, "expand", {}).get("kebab_place")
                    if not p:
                        continue
                    g_id = getattr(p, 'google_place_id', '')
                    if not g_id or g_id in seen_ids:
                        continue
                    seen_ids.add(g_id)
                    
                    # City name extraction
                    city_name = "Unknown"
                    city_data = getattr(getattr(p, "expand", {}), 'get', lambda x: None)('city') if hasattr(getattr(p, "expand", {}), 'get') else None
                    if not city_data:
                        expanded = getattr(p, "expand", {})
                        if isinstance(expanded, dict):
                            city_data = expanded.get('city')
                    
                    if city_data:
                        city_name = getattr(city_data, 'name', city_data.get('name', 'Unknown') if isinstance(city_data, dict) else 'Unknown')
                    
                    if city_name == "Unknown" and hasattr(p, 'city') and p.city:
                        try:
                            city_rec = self.client.collection('cities').get_one(p.city)
                            city_name = getattr(city_rec, 'name', 'Unknown')
                        except: pass
                    
                    if city_name == "Unknown" and hasattr(p, 'address') and p.address:
                        all_cities = self.client.collection('cities').get_full_list()
                        for c in all_cities:
                            if getattr(c, 'name', '').lower() in p.address.lower():
                                city_name = getattr(c, 'name', 'Unknown')
                                break

                    unique_items.append({
                        'id': p.id,
                        'name': p.name,
                        'address': p.address,
                        'city': city_name,
                        'google_place_id': g_id,
                        'latitude': getattr(p, 'lat', 0),
                        'longitude': getattr(p, 'lng', 0),
                        'photo_url': self.get_file_url(p, getattr(p, 'photo', '')),
                        'rating': r.rating,
                        'total_reviews': r.total_reviews,
                        'rank_score': r.rank_score,
                        'ai_score': getattr(r, 'ai_score', r.rank_score),
                        'has_ai_analysis': getattr(r, 'ai_score', 0) > 0,
                        'opening_hours': getattr(p, 'opening_hours', None),
                        'global_rank': 0
                    })
                
                # Step 4: Sort by rank_score descending, then take top N
                unique_items.sort(key=lambda x: (x['rank_score'], x['total_reviews']), reverse=True)
                results = unique_items[:limit]
                
                # Step 5: Set global rank
                for i, r in enumerate(results):
                    r['global_rank'] = i + 1
                
                return results
            
            result = self._execute_with_auth_retry(_get_global_rankings)
            if result is None:
                return []
            return result
        except Exception as e:
            print(f"Error getting global rankings: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_most_recent_update(self) -> Optional[datetime]:
        """Get latest update time from ratings"""
        try:
            # Use auth retry wrapper
            def _get_most_recent_update():
                record = self.client.collection('ratings').get_first_list_item("", query_params={"sort": "-created"})
                if record:
                    # Pocketbase uses 'created' as a string: 'YYYY-MM-DD HH:MM:SS.mmmZ'
                    # Convert to datetime
                    try:
                        return datetime.strptime(record.created, "%Y-%m-%d %H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                    except ValueError:
                        return datetime.strptime(record.created, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=timezone.utc)
                return None
            
            return self._execute_with_auth_retry(_get_most_recent_update)
        except Exception as e:
            pass
        return None

    def get_last_update_time(self, city_name: str) -> Optional[datetime]:
        """Get latest update time for city"""
        # For simplicity, returning global latest or implement filtering
        return self.get_most_recent_update()

    def get_file_url(self, record, filename: str) -> Optional[str]:
        if not filename: return None
        # PB URL format: /api/files/COLLECTION_ID/RECORD_ID/FILENAME
        return f"{self.url}/api/files/{record.collection_id}/{record.id}/{filename}"

    def _format_record(self, record):
        """Convert a Pocketbase record object to a plain dict"""
        # Current version of pocketbase-python-sdk stores fields directly in __dict__
        data = record.__dict__.copy()
        # Ensure ID is there
        data['id'] = record.id
        # Optional: Remove internal Pocketbase fields to stay clean
        # but keep them if they don't hurt.
        return data

    def get_all_recent_ratings(self) -> List[Dict]:
        """Get the latest rating for EVERY kebab place in the database."""
        try:
            # Use auth retry wrapper
            def _get_all_recent_ratings():
                # This is used for global ranking recalculations.
                # We want the latest rating for each place.
                # Fetch last 10,000 ratings (enough to cover all 6,000 places)
                records = self.client.collection('ratings').get_list(
                    1, 10000,
                    query_params={
                        "sort": "-created",
                        "expand": "kebab_place"
                    }
                )
                
                results = []
                seen_places = set()
                for r in records.items:
                    p = getattr(r, "expand", {}).get("kebab_place")
                    if not p or p.id in seen_places: continue
                    seen_places.add(p.id)
                    
                    results.append({
                        'rating_id': r.id,
                        'place_id': p.id,
                        'google_place_id': p.google_place_id,
                        'name': p.name,
                        'rating': r.rating,
                        'total_reviews': r.total_reviews,
                        'rank_score': r.rank_score
                    })
                return results
            
            result = self._execute_with_auth_retry(_get_all_recent_ratings)
            if result is None:
                return []
            return result
        except Exception as e:
            print(f"Error in get_all_recent_ratings: {e}")
            return []

    # Helper for direct client usage in app.py
    # AI Analysis methods
    def get_city_ai_summary(self, city_name: str):
        """Get summarized AI data for a city by querying ai_analysis collection directly."""
        self._ensure_auth()
        try:
            city_id = self.get_city_id(city_name)
            if not city_id: return None
            
            # Query AI analysis directly, expanding kebab_place to filter by city
            analyses_records = self.client.collection('ai_analysis').get_full_list(
                query_params={
                    "filter": f'kebab_place.city="{city_id}"',
                    "expand": "kebab_place"
                }
            )
            
            if not analyses_records: return None
            
            # Detailed stats
            total_sentiment = 0
            authenticity_scores = []
            trending_up, trending_down = 0, 0
            
            for a in analyses_records:
                data = a.analysis_data if isinstance(a.analysis_data, dict) else {}
                sentiment_analysis = data.get('sentiment_analysis', {})
                authenticity_analysis = data.get('authenticity_analysis', {})
                trend_analysis = data.get('trend_analysis', {})

                total_sentiment += sentiment_analysis.get('score', 0)
                if 'score' in authenticity_analysis:
                    authenticity_scores.append(authenticity_analysis.get('score', 0))
                
                trend = trend_analysis.get('trend', 'stable')
                if trend == 'improving':
                    trending_up += 1
                elif trend == 'declining':
                    trending_down += 1
            
            num_analyzed = len(analyses_records)
            avg_sentiment = total_sentiment / num_analyzed if num_analyzed > 0 else 0
            sentiment_label = "pozytywny" if avg_sentiment > 0.1 else "negatywny" if avg_sentiment < -0.1 else "neutralny"

            return {
                'kebabs_analyzed': num_analyzed,
                'average_sentiment': round(avg_sentiment, 2),
                'average_authenticity': round(sum(authenticity_scores) / len(authenticity_scores) * 100, 1) if authenticity_scores else 100,
                'trending_up_count': trending_up,
                'trending_down_count': trending_down,
                'summary': f"W {city_name} przeanalizowano {num_analyzed} kebabów. "
                           f"Ogólny nastrój klientów jest {sentiment_label}. "
                           f"{trending_up} miejsc poprawia jakość, a {trending_down} notuje spadki."
            }
        except Exception as e:
            print(f"Error in get_city_ai_summary: {e}")
            return None

    def get_place_id(self, google_place_id: str) -> Optional[str]:
        """Get Pocketbase ID for a kebab place"""
        self._ensure_auth()
        try:
            place = self.client.collection('kebab_places').get_first_list_item(f'google_place_id="{google_place_id}"')
            return place.id
        except:
            return None

    def get_city_rankings_history(self, city_name: str) -> List[Dict]:
        """Get historical rankings for all kebab places in a city."""
        self._ensure_auth()
        try:
            city_id = self.get_city_id(city_name)
            if not city_id: return []
            
            # Fetch ratings directly, sorted by place and then created
            # This avoids the slow reverse expansion
            ratings = self.client.collection('ratings').get_full_list(
                query_params={
                    "filter": f'kebab_place.city="{city_id}"',
                    "sort": "kebab_place,-created",
                    "expand": "kebab_place"
                }
            )
            
            # Group by place in Python
            history_map = {}
            for r in ratings:
                p = getattr(r, "expand", {}).get("kebab_place")
                if not p: continue
                
                if p.id not in history_map:
                    history_map[p.id] = {
                        'place_id': p.id,
                        'name': p.name,
                        'google_place_id': p.google_place_id,
                        'ratings': []
                    }
                
                history_map[p.id]['ratings'].append({
                    'rating': r.rating,
                    'total_reviews': r.total_reviews,
                    'rank_score': r.rank_score,
                    'city_rank': getattr(r, 'city_rank', 0),
                    'data_fetched_at': r.created
                })
            
            return list(history_map.values())
        except Exception as e:
            print(f"Error in get_city_rankings_history: {e}")
            return []

    def get_places_by_google_ids(self, google_ids: List[str]) -> List[Dict]:
        """Fetch multiple places by their google_ids"""
        self._ensure_auth()
        try:
            filters = " || ".join([f'google_place_id="{id}"' for id in google_ids])
            records = self.client.collection('kebab_places').get_full_list(query_params={"filter": filters})
            return [self._format_record(r) for r in records]
        except:
            return []

    def get_previous_rankings(self, city_name: str) -> Dict[str, int]:
        """Get the most recent rankings before the current update for badge calculation."""
        self._ensure_auth()
        try:
            city_id = self.get_city_id(city_name)
            if not city_id: return {}
            
            # Find the two latest distinct created timestamps in this city
            last_ratings = self.client.collection('ratings').get_list(
                1, 200, # Large batch to find distinct timestamps
                query_params={
                    "filter": f'kebab_place.city="{city_id}"',
                    "sort": "-created"
                }
            )
            
            if not last_ratings.items: return {}
            
            timestamps = sorted(list(set(r.created for r in last_ratings.items)), reverse=True)
            if len(timestamps) < 2: return {}
            
            previous_timestamp = timestamps[1]
            
            # Fetch all ratings from that previous timestamp
            prev_records = self.client.collection('ratings').get_full_list(
                query_params={
                    "filter": f'kebab_place.city="{city_id}" && created="{previous_timestamp}"',
                    "expand": "kebab_place"
                }
            )
            
            return {getattr(r, "expand", {}).get("kebab_place").google_place_id: getattr(r, "city_rank", 0) 
                    for r in prev_records if getattr(r, "expand", {}).get("kebab_place")}
        except Exception as e:
            print(f"Error in get_previous_rankings: {e}")
            return {}

    def get_all_recent_ratings(self) -> List[Dict]:
        """Get the latest rating for EVERY kebab place in the database"""
        try:
            places = self.client.collection('kebab_places').get_full_list(
                query_params={"expand": "ratings(kebab_place),city"}
            )
            
            results = []
            for p in places:
                expanded = getattr(p, "expand", {})
                ratings_list = expanded.get("ratings(kebab_place)", [])
                if not ratings_list: continue
                
                r = sorted(ratings_list, key=lambda x: x.created, reverse=True)[0]
                city_name = expanded.get('city', {}).name if 'city' in expanded else "Unknown"

                results.append({
                    'id': p.id,
                    'rating_id': r.id,
                    'name': p.name,
                    'rating': r.rating,
                    'total_reviews': r.total_reviews,
                    'rank_score': r.rank_score,
                    'city': city_name,
                    'google_place_id': p.google_place_id
                })
            return results
        except Exception as e:
            print(f"Error in get_all_recent_ratings: {e}")
            return []

    def update_global_rank(self, rating_id: str, global_rank: int):
        """Update global rank for a specific rating record"""
        self._ensure_auth()
        try:
            self.client.collection('ratings').update(rating_id, {"global_rank": global_rank})
        except Exception as e:
            print(f"Error in update_global_rank: {e}")

    def upsert_ai_analysis(self, kebab_place_id: str, ai_analysis: Dict, ai_score: float, ai_summary: str):
        """Store or update AI analysis for a place"""
        self._ensure_auth()
        try:
            # Check if exists
            try:
                existing = self.client.collection('ai_analysis').get_first_list_item(f'kebab_place="{kebab_place_id}"')
                self.client.collection('ai_analysis').update(existing.id, {
                    "analysis_data": ai_analysis,
                    "ai_score": ai_score,
                    "ai_summary": ai_summary,
                    "confidence_score": ai_analysis.get('ai_confidence_score', 0)
                })
            except:
                self.client.collection('ai_analysis').create({
                    "kebab_place": kebab_place_id,
                    "analysis_data": ai_analysis,
                    "ai_score": ai_score,
                    "ai_summary": ai_summary,
                    "confidence_score": ai_analysis.get('ai_confidence_score', 0)
                })
        except Exception as e:
            print(f"Error in upsert_ai_analysis: {e}")

    def update_rating_ai_data(self, kebab_place_id: str, ai_score: float, ai_confidence: float):
        """Update the latest rating record with AI scores"""
        self._ensure_auth()
        try:
            # Find latest rating
            ratings = self.client.collection('ratings').get_full_list(
                query_params={
                    "filter": f'kebab_place="{kebab_place_id}"',
                    "sort": "-created",
                    "limit": 1
                }
            )
            if ratings:
                self.client.collection('ratings').update(ratings[0].id, {
                    "ai_score": ai_score
                })
        except Exception as e:
            print(f"Error in update_rating_ai_data: {e}")

    def delete_ai_analysis_for_city(self, city_id: str):
        """Delete all AI analysis records for places in a city"""
        self._ensure_auth()
        try:
            places = self.client.collection('kebab_places').get_full_list(query_params={"filter": f'city="{city_id}"'})
            for p in places:
                try:
                    ai = self.client.collection('ai_analysis').get_first_list_item(f'kebab_place="{p.id}"')
                    self.client.collection('ai_analysis').delete(ai.id)
                except:
                    pass
        except Exception as e:
            print(f"Error in delete_ai_analysis_for_city: {e}")

    def upsert_cached_review(self, data: Dict):
        """Cache a review in Pocketbase"""
        self._ensure_auth()
        try:
            # Hash author for privacy if not already hashed
            author_id = data.get('author_id')
            
            # Simple check/upsert
            try:
                existing = self.client.collection('cached_reviews').get_first_list_item(
                    f'google_place_id="{data["google_place_id"]}" && author_name="{data["author_name"]}"'
                )
                self.client.collection('cached_reviews').update(existing.id, data)
            except:
                self.client.collection('cached_reviews').create(data)
        except Exception as e:
            # Collection might not exist, ignore for now
            pass

    def get_ai_insights(self, google_place_id: str):
        """Get AI insights for a specific place"""
        self._ensure_auth()
        try:
            place = self.client.collection('kebab_places').get_first_list_item(
                f'google_place_id="{google_place_id}"',
                query_params={"expand": "ai_analysis(kebab_place)"}
            )
            expanded = getattr(place, "expand", {})
            ai_list = expanded.get("ai_analysis(kebab_place)", [])
            if ai_list:
                return self._format_record(ai_list[0])
        except Exception as e:
            # print(f"Error in get_ai_insights: {e}")
            pass
        return None

    def get_ai_for_places(self, google_place_ids: List[str]) -> Dict[str, Dict]:
        """Fetch AI analysis for a list of google_place_ids at once."""
        self._ensure_auth()
        if not google_place_ids: return {}
        try:
            # Join IDs into filter string.
            # Handle potential escaping if IDs contain weird characters (though Google IDs usually don't)
            id_filters = " || ".join([f'kebab_place.google_place_id="{gid}"' for gid in google_place_ids])
            
            # Fetch AI analysis records and expand the linked kebab place
            ai_records = self.client.collection('ai_analysis').get_full_list(
                query_params={
                    "filter": f"({id_filters})",
                    "expand": "kebab_place"
                }
            )
            
            result = {}
            for rec in ai_records:
                place = getattr(rec, "expand", {}).get("kebab_place")
                if place:
                    result[place.google_place_id] = self._format_record(rec)
            return result
        except Exception as e:
            print(f"Error in get_ai_for_places: {e}")
            return {}

    def upsert_kebab_place(self, google_place_id: str, name: str, address: str,
                          city_id: str, latitude: float, longitude: float,
                          photo_url: Optional[str] = None,
                          opening_hours: Optional[str] = None) -> str:
        """Insert or update a kebab place in Pocketbase"""
        self._ensure_auth()
        extra = {}
        if opening_hours is not None:
            extra["opening_hours"] = opening_hours
        # photo is a PocketBase File field (binary storage) — not updated here
        try:
            # Check if place exists
            try:
                # 1. Primary match by Google Place ID
                existing = self.client.collection('kebab_places').get_first_list_item(f'google_place_id="{google_place_id}"')
                self.client.collection('kebab_places').update(existing.id, {
                    "name": name,
                    "address": address,
                    "city": city_id,
                    "lat": latitude,
                    "lng": longitude,
                    **extra,
                })
                return existing.id
            except:
                # 2. Secondary match by Name + City (prevents duplicates if API ID changed)
                try:
                    safe_name = name.replace('"', '\\"')
                    existing = self.client.collection('kebab_places').get_first_list_item(f'name="{safe_name}" && city="{city_id}"')
                    self.client.collection('kebab_places').update(existing.id, {
                        "google_place_id": google_place_id,
                        "address": address,
                        "lat": latitude,
                        "lng": longitude,
                        **extra,
                    })
                    return existing.id
                except:
                    # 3. Create New
                    new_record = self.client.collection('kebab_places').create({
                        "google_place_id": google_place_id,
                        "name": name,
                        "address": address,
                        "city": city_id,
                        "lat": latitude,
                        "lng": longitude,
                        **extra,
                    })
                    return new_record.id
        except Exception as e:
            print(f"Error upserting kebab place: {e}")
            raise

    def insert_rating_history(self, kebab_place_id: str, rating: float, total_reviews: int,
                            positive_percentage: float, rank_score: float, city_rank: int, 
                            update_batch_timestamp: Optional[str] = None):
        """Insert a new rating record in Pocketbase, or update if one exists in the last hour."""
        self._ensure_auth()
        try:
            # Check for a very recent record (last 60 mins) to avoid duplication
            # if the script is run multiple times.
            from datetime import datetime, timedelta, timezone
            now = datetime.now(timezone.utc)
            hour_ago = (now - timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S')
            
            recent = self.client.collection('ratings').get_list(1, 1, {
                "filter": f'kebab_place="{kebab_place_id}" && created >= "{hour_ago}"',
                "sort": "-created"
            })
            
            data = {
                "kebab_place": kebab_place_id,
                "rating": rating,
                "total_reviews": total_reviews,
                "rank_score": rank_score,
                "city_rank": city_rank
                # ai_score is handled separately or byAIDataUpdater
            }
            
            if recent.items:
                # Update the most recent one
                return self.client.collection('ratings').update(recent.items[0].id, data)
            else:
                # Create new
                return self.client.collection('ratings').create(data)
        except Exception as e:
            print(f"Error handling rating history: {e}")
            raise

    def recalculate_city_rankings(self, city_id: str):
        """Recalculate rankings for all kebabs in a city using Pocketbase."""
        self._ensure_auth()
        try:
            # Query latest ratings for this city
            ratings = self.client.collection('ratings').get_full_list(
                query_params={
                    "filter": f'kebab_place.city="{city_id}"',
                    "sort": "-created,-rank_score",
                    "expand": "kebab_place"
                }
            )
            
            if not ratings: return
            
            # Distinct by place, keeping latest
            latest_ratings = {}
            for r in ratings:
                p_id = r.kebab_place
                if p_id not in latest_ratings:
                    latest_ratings[p_id] = r
            
            # Sort by rank_score
            sorted_ratings = sorted(latest_ratings.values(), key=lambda x: (x.rank_score, x.total_reviews), reverse=True)
            
            # Update city_rank in Pocketbase
            for i, r in enumerate(sorted_ratings):
                try:
                    self.client.collection('ratings').update(r.id, {"city_rank": i + 1})
                except Exception as e:
                    print(f"Error updating rank for {r.id}: {e}")
        except Exception as e:
            print(f"Error recalculating city rankings: {e}")

    def reset_city_ranks(self, city_id: str):
        """Reset city_rank to 0 in the latest rating for all places in a city before updating.
        This marks all places as 'ghost' so only re-validated places become visible after update.
        Works on the ratings collection (where city_rank actually lives in the original schema)."""
        self._ensure_auth()
        try:
            print(f"Resetting existing city ranks for city ID: {city_id}...")
            places = self.client.collection('kebab_places').get_full_list(
                query_params={"filter": f'city="{city_id}"'}
            )
            count = 0
            for p in places:
                try:
                    latest = self.client.collection('ratings').get_list(1, 1, {
                        "filter": f'kebab_place="{p.id}"',
                        "sort": "-created"
                    })
                    if latest.items:
                        l = latest.items[0]
                        # CREATE A NEW RECORD instead of updating.
                        # This preserves history for trends.
                        self.client.collection('ratings').create({
                            "kebab_place": p.id,
                            "rating": getattr(l, 'rating', 0),
                            "total_reviews": getattr(l, 'total_reviews', 0),
                            "rank_score": getattr(l, 'rank_score', 0),
                            "city_rank": 0
                        })
                        count += 1
                except Exception as reset_err:
                    print(f"  Warning: Could not reset rank for {getattr(p, 'name', p.id)}: {reset_err}")
            print(f"\u2713 Reset ranks for {count} places.")
        except Exception as e:
            print(f"Error resetting city ranks: {e}")

    def upload_place_photo(self, record_id: str, photo_url: str) -> bool:
        """Download photo from URL and upload to PocketBase record"""
        self._ensure_auth()
        if not photo_url or photo_url == 'NONE':
            return False
            
        try:
            # Download the image
            response = requests.get(photo_url, stream=True, timeout=15)
            if response.status_code != 200:
                print(f"  Failed to download photo: {response.status_code}")
                return False
                
            # Create a temporary file to store the image
            # Get extension from URL or default to .jpg
            ext = '.jpg'
            if '.png' in photo_url.lower(): ext = '.png'
            elif '.webp' in photo_url.lower(): ext = '.webp'
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                for chunk in response.iter_content(chunk_size=8192):
                    tmp.write(chunk)
                tmp_path = tmp.name
                
            try:
                # Upload to PocketBase
                # Files are passed as a tuple: (filename, fileobj)
                with open(tmp_path, 'rb') as f:
                    self.client.collection('kebab_places').update(record_id, {
                        'photo': ('photo' + ext, f)
                    })
                return True
            finally:
                # Cleanup temp file
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                    
        except Exception as e:
            print(f"  Error uploading photo for {record_id}: {e}")
            return False