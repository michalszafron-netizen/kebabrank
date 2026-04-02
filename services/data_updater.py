# services/data_updater.py
from datetime import datetime
import threading
import schedule
import time
import os

class DataUpdater:
    def __init__(self, google_service, db_service, ranking_service):
        self.google_service = google_service
        self.db_service = db_service
        self.ranking_service = ranking_service
        self.is_updating = False
        
    def update_city_data(self, city_name: str):
        """Update data for a specific city"""
        if self.is_updating:
            return
        
        try:
            self.is_updating = True
            batch_timestamp = datetime.now().isoformat()
            print(f"Updating data for {city_name}... Batch: {batch_timestamp}")
            
            # Get city ID
            city_id = self.db_service.get_city_id(city_name)
            if not city_id:
                print(f"City {city_name} not found in database")
                return
            
            # Fetch kebab places from Google
            kebabs = self.google_service.search_kebabs_in_city(city_name)
            print(f"DEBUG: Found {len(kebabs)} kebabs from Google for {city_name}")
            
            # Filter quality kebabs
            quality_kebabs = self.ranking_service.filter_quality_kebabs(kebabs)
            print(f"DEBUG: {len(quality_kebabs)} kebabs passed quality filter")
            
            # Get previous rankings for badge calculation
            previous_rankings = self.db_service.get_previous_rankings(city_name)
            print(f"Found {len(previous_rankings)} previous rankings for badge calculation")
            
            # Rank kebabs with previous rankings for proper badge calculation
            ranked_kebabs = self.ranking_service.rank_kebabs(quality_kebabs, previous_rankings)
            print(f"DEBUG: {len(ranked_kebabs)} kebabs ranked and ready for database")
            
            # Start transaction
            print("Starting database transaction...")
            transaction_data = {
                'city_id': city_id,
                'kebabs': [],
                'success': False
            }
            
            try:
                # Save to database in transaction
                for kebab in ranked_kebabs:
                    # Insert or update kebab place
                    place_id = self.db_service.upsert_kebab_place(
                        google_place_id=kebab['place_id'],
                        name=kebab['name'],
                        address=kebab['address'],
                        city_id=city_id,
                        latitude=kebab['location']['lat'],
                        longitude=kebab['location']['lng']
                    )
                    
                    # Insert rating history
                    self.db_service.insert_rating_history(
                        kebab_place_id=place_id,
                        rating=kebab['rating'],
                        total_reviews=kebab['total_reviews'],
                        positive_percentage=kebab['positive_percentage'],
                        rank_score=kebab['rank_score'],
                        city_rank=kebab['city_rank'],
                        update_batch_timestamp=batch_timestamp
                    )
                    
                    transaction_data['kebabs'].append({
                        'place_id': place_id,
                        'name': kebab['name']
                    })
                
                # Recalculate rankings
                print(f"Recalculating rankings for all kebabs in {city_name}...")
                self.db_service.recalculate_city_rankings(city_id)
                
                # Update global rankings
                self._update_global_rankings()
                
                print(f"✓ Successfully updated {len(ranked_kebabs)} kebabs for {city_name}")
                
            except Exception as e:
                print(f"✗ Update failed for {city_name}: {e}")
                raise
                
        except Exception as e:
            print(f"Error updating city data: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_updating = False
            
    def _cleanup_failed_transaction(self, transaction_data):
        """No-op for Pocketbase as we use individual upserts"""
        pass
    
    def update_all_cities(self):
        """Update data for all cities"""
        cities = self.db_service.get_cities()
        for city in cities:
            self.update_city_data(city['name'])
            time.sleep(5)  # Rate limiting between cities
    
    def _update_global_rankings(self):
        """Recalculate global rankings - with graceful error handling"""
        try:
            print("🔄 Attempting to update global rankings...")
            
            # Get all recent kebab ratings
            all_kebabs = self.db_service.get_all_recent_ratings()
            
            if not all_kebabs:
                print("⚠️  No recent ratings found for global rankings")
                return
                
            # Rank globally
            ranked_globally = self.ranking_service.rank_kebabs(all_kebabs)
            
            # Update global ranks in database with error handling per record
            success_count = 0
            error_count = 0
            
            for i, kebab in enumerate(ranked_globally):
                try:
                    # Skip if rating_id is missing
                    if 'rating_id' not in kebab:
                        print(f"⚠️  Skipping global rank update for {kebab.get('name', 'Unknown')} - missing rating_id")
                        error_count += 1
                        continue
                        
                    self.db_service.update_global_rank(
                        rating_id=kebab['rating_id'],
                        global_rank=i + 1  # Use sequential global rank
                    )
                    success_count += 1
                    
                except Exception as record_error:
                    print(f"⚠️  Failed to update global rank for {kebab.get('name', 'Unknown')}: {record_error}")
                    error_count += 1
                    # Continue with next record even if one fails
                    continue
                    
            print(f"✅ Global rankings: {success_count} updated, {error_count} failed")
            
        except Exception as e:
            print(f"⚠️  Global rankings update failed (non-critical): {e}")
            print("💡 This won't affect city rankings or badge calculations")
    
    def start_scheduled_updates(self):
        """Start background scheduled updates every 3 days"""
        def run_updates():
            while True:
                schedule.run_pending()
                time.sleep(3600)  # Check every hour
        
        # Schedule updates every 7 days
        update_interval = int(os.getenv('DATABASE_UPDATE_INTERVAL_DAYS', 7))
        schedule.every(update_interval).days.do(self.update_all_cities)
        
        # Run in background thread
        update_thread = threading.Thread(target=run_updates, daemon=True)
        update_thread.start()
