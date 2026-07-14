#!/usr/bin/env python3
"""
Historical Data Generator for Kebab Rank
Creates realistic historical data to simulate 2 weeks of ranking changes
"""

import sys
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

# Add current directory to path
sys.path.append('.')

try:
    from supabase import create_client, Client
except ImportError:
    from supabase.client import Client, create_client

from services.database import DatabaseService


class HistoricalDataGenerator:
    def __init__(self, supabase_url: str, supabase_key: str):
        """Initialize the historical data generator"""
        self.db_service = DatabaseService(supabase_url, supabase_key)
        self.client = self.db_service.client
        
    def get_current_rankings(self, city_name: str) -> List[Dict]:
        """Get current rankings for a city"""
        try:
            rankings = self.db_service.get_city_rankings(city_name, limit=100)
            print(f"Found {len(rankings)} current kebabs in {city_name}")
            return rankings
        except Exception as e:
            print(f"Error getting current rankings: {e}")
            return []
    
    def generate_realistic_historical_data(self, city_name: str, days_ago: int = 14, preview_only: bool = True) -> Dict:
        """
        Generate realistic historical data for a city
        
        Strategy:
        - 60%: Small changes (±1-2 positions)
        - 20%: No change (stable top performers)
        - 15%: Moderate changes (±3-5 positions)
        - 5%: New entries (1-2 per city)
        - Ratings change slightly (±0.1-0.3 stars)
        - Review counts increase by 5-20%
        """
        
        current_rankings = self.get_current_rankings(city_name)
        if not current_rankings:
            return {"error": f"No current rankings found for {city_name}"}
        
        # Get city ID
        city_id = self.db_service.get_city_id(city_name)
        if not city_id:
            return {"error": f"City {city_name} not found"}
        
        # Calculate historical date
        historical_date = datetime.now() - timedelta(days=days_ago)
        
        # Create realistic historical rankings
        historical_data = []
        changes_summary = {
            "city": city_name,
            "historical_date": historical_date.isoformat(),
            "total_kebabs": len(current_rankings),
            "changes": {
                "no_change": 0,
                "small_change": 0,
                "moderate_change": 0,
                "new_entries": 0
            },
            "preview": []
        }
        
        # Determine which kebabs will be "new" (not in historical data)
        total_kebabs = len(current_rankings)
        new_entries_count = max(1, min(2, total_kebabs // 20))  # 5% but at least 1, max 2
        
        # Randomly select which kebabs will be new
        new_kebab_indices = random.sample(range(total_kebabs), new_entries_count)
        
        for i, current_kebab in enumerate(current_rankings):
            if i in new_kebab_indices:
                # This kebab is "new" - won't appear in historical data
                changes_summary["changes"]["new_entries"] += 1
                changes_summary["preview"].append({
                    "name": current_kebab["name"],
                    "current_rank": current_kebab["city_rank"],
                    "historical_rank": "NEW",
                    "change": "NEW",
                    "rating_change": 0,
                    "review_change": 0
                })
                continue
            
            # Determine type of change
            change_type = random.choices(
                ["no_change", "small_change", "moderate_change"],
                weights=[0.2, 0.6, 0.15],
                k=1
            )[0]
            
            current_rank = current_kebab["city_rank"]
            current_rating = current_kebab.get("rating", 4.0)
            current_reviews = current_kebab.get("total_reviews", 100)
            
            # Generate historical rank
            if change_type == "no_change":
                historical_rank = current_rank
                rank_change = 0
                changes_summary["changes"]["no_change"] += 1
            elif change_type == "small_change":
                # Small change: ±1-2 positions
                rank_change = random.choice([-2, -1, 1, 2])
                historical_rank = max(1, current_rank + rank_change)
                changes_summary["changes"]["small_change"] += 1
            else:  # moderate_change
                # Moderate change: ±3-5 positions
                rank_change = random.choice([-5, -4, -3, 3, 4, 5])
                historical_rank = max(1, current_rank + rank_change)
                changes_summary["changes"]["moderate_change"] += 1
            
            # Adjust rating slightly (±0.1-0.3)
            rating_change = round(random.uniform(-0.3, 0.3), 1)
            historical_rating = max(1.0, min(5.0, current_rating + rating_change))
            
            # Adjust review count (5-20% decrease for historical data)
            review_change_percent = random.uniform(-0.2, -0.05)  # 5-20% fewer reviews in the past
            historical_reviews = max(1, int(current_reviews * (1 + review_change_percent)))
            
            # Create historical record
            historical_record = {
                "google_place_id": current_kebab["google_place_id"],
                "name": current_kebab["name"],
                "historical_rank": historical_rank,
                "current_rank": current_rank,
                "rank_change": rank_change,
                "historical_rating": historical_rating,
                "current_rating": current_rating,
                "rating_change": rating_change,
                "historical_reviews": historical_reviews,
                "current_reviews": current_reviews,
                "review_change": current_reviews - historical_reviews,
                "data_fetched_at": historical_date.isoformat()
            }
            
            historical_data.append(historical_record)
            
            # Add to preview
            change_indicator = "↑" if rank_change > 0 else "↓" if rank_change < 0 else "→"
            changes_summary["preview"].append({
                "name": current_kebab["name"],
                "current_rank": current_rank,
                "historical_rank": historical_rank,
                "change": f"{change_indicator} {abs(rank_change)}" if rank_change != 0 else "→ 0",
                "rating_change": f"{rating_change:+.1f}",
                "review_change": f"+{current_reviews - historical_reviews}"
            })
        
        changes_summary["historical_data_count"] = len(historical_data)
        
        if not preview_only:
            # Actually insert the historical data
            inserted_count = self._insert_historical_data(historical_data, city_id)
            changes_summary["inserted_count"] = inserted_count
        
        return changes_summary
    
    def _insert_historical_data(self, historical_data: List[Dict], city_id: int) -> int:
        """Insert historical data into the database"""
        inserted_count = 0
        
        for record in historical_data:
            try:
                # Get kebab place ID
                place_response = self.client.table('kebab_places').select('id').eq(
                    'google_place_id', record['google_place_id']
                ).execute()
                
                if not place_response.data:
                    print(f"Warning: Kebab place not found for {record['name']}")
                    continue
                
                kebab_place_id = place_response.data[0]['id']
                
                # Calculate rank score (similar to current logic)
                rank_score = self._calculate_rank_score(
                    record['historical_rating'],
                    record['historical_reviews']
                )
                
                # Insert historical rating
                response = self.client.table('ratings_history').insert({
                    'kebab_place_id': kebab_place_id,
                    'rating': record['historical_rating'],
                    'total_reviews': record['historical_reviews'],
                    'positive_percentage': 80.0,  # Default value
                    'rank_score': rank_score,
                    'city_rank': record['historical_rank'],
                    'data_fetched_at': record['data_fetched_at']
                }).execute()
                
                if response.data:
                    inserted_count += 1
                    print(f"✓ Added historical data for {record['name']} (Rank: {record['historical_rank']})")
                else:
                    print(f"✗ Failed to insert historical data for {record['name']}")
                    
            except Exception as e:
                print(f"Error inserting historical data for {record['name']}: {e}")
        
        return inserted_count
    
    def _calculate_rank_score(self, rating: float, total_reviews: int) -> float:
        """Calculate rank score similar to the current system"""
        # This mimics the ranking logic from the ranking service
        base_score = rating * 20  # Rating contributes more
        review_bonus = min(total_reviews * 0.01, 10)  # Review count bonus, capped
        return base_score + review_bonus
    
    def backup_current_data(self) -> bool:
        """Create a backup of current ratings_history data"""
        try:
            # Get all current ratings
            response = self.client.table('ratings_history').select('*').execute()
            
            if response.data:
                backup_file = f"ratings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(response.data, f, indent=2, ensure_ascii=False)
                
                print(f"✓ Backup created: {backup_file}")
                return True
            else:
                print("No data to backup")
                return False
                
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def validate_historical_data(self, city_name: str) -> Dict:
        """Validate that historical data was created correctly"""
        try:
            # Test the ranking system to see if it now shows proper changes
            rankings = self.db_service.get_city_rankings(city_name, limit=10)
            
            validation_result = {
                "city": city_name,
                "total_rankings": len(rankings),
                "rankings_with_changes": 0,
                "new_entries": 0,
                "stable_entries": 0,
                "sample_data": []
            }
            
            for kebab in rankings[:5]:  # Sample first 5
                validation_result["sample_data"].append({
                    "name": kebab["name"],
                    "current_rank": kebab.get("city_rank"),
                    "rank_change": kebab.get("rank_change"),
                    "is_new": kebab.get("is_new", False),
                    "change_indicator": kebab.get("rank_change_indicator", "unknown")
                })
                
                if kebab.get("is_new"):
                    validation_result["new_entries"] += 1
                elif kebab.get("rank_change") is not None:
                    validation_result["rankings_with_changes"] += 1
                else:
                    validation_result["stable_entries"] += 1
            
            return validation_result
            
        except Exception as e:
            return {"error": f"Validation failed: {e}"}


def main():
    """Main function to run the historical data generator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate realistic historical kebab ranking data')
    parser.add_argument('--city', action='append', help='City name to generate data for (can be used multiple times)')
    parser.add_argument('--all-cities', action='store_true', help='Generate data for all cities')
    parser.add_argument('--exclude', action='append', help='City names to exclude (can be used multiple times)')
    parser.add_argument('--days-ago', type=int, default=14, help='How many days ago to backdate')
    parser.add_argument('--preview', action='store_true', help='Preview changes without applying')
    parser.add_argument('--apply', action='store_true', help='Apply the changes to database')
    parser.add_argument('--backup', action='store_true', help='Create backup before applying')
    parser.add_argument('--validate', action='store_true', help='Validate after applying')
    parser.add_argument('--batch-delay', type=int, default=2, help='Delay between cities in seconds (default: 2)')
    
    args = parser.parse_args()
    
    # Load environment variables from .env file
    def load_env_file():
        """Simple .env file loader"""
        try:
            # Try current directory first
            env_path = '.env'
            if not os.path.exists(env_path):
                # Try parent directory
                env_path = '../.env'
            
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            print(f"✓ Loaded environment variables from {env_path}")
            return True
        except FileNotFoundError:
            print("⚠ .env file not found, using system environment variables")
            return False
        except Exception as e:
            print(f"⚠ Error loading .env file: {e}, using system environment variables")
            return False
    
    # Try to load from .env file
    env_loaded = load_env_file()
    
    # Debug: Print current environment variables
    print(f"DEBUG: SUPABASE_URL available: {'YES' if os.getenv('SUPABASE_URL') else 'NO'}")
    print(f"DEBUG: SUPABASE_KEY available: {'YES' if os.getenv('SUPABASE_KEY') else 'NO'}")
    
    # Check environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY environment variables required")
        print("Make sure your .env file contains these variables:")
        print("SUPABASE_URL=https://your-supabase-url.supabase.co")
        print("SUPABASE_KEY=your-supabase-key-here")
        sys.exit(1)
    
    generator = HistoricalDataGenerator(supabase_url, supabase_key)
    
    # Determine which cities to process
    cities_to_process = []
    
    if args.all_cities:
        # Get all cities from database
        all_cities = generator.db_service.get_cities()
        if not all_cities:
            print("Error: No cities found in database")
            sys.exit(1)
        
        cities_to_process = [city['name'] for city in all_cities]
        print(f"Found {len(cities_to_process)} cities in database")
        
        # Exclude specified cities
        if args.exclude:
            cities_to_process = [city for city in cities_to_process if city not in args.exclude]
            print(f"Excluded cities: {args.exclude}")
            print(f"Processing {len(cities_to_process)} cities after exclusions")
    
    elif args.city:
        # Use specified cities
        cities_to_process = args.city
        print(f"Processing specified cities: {cities_to_process}")
    
    else:
        # Default to Warszawa
        cities_to_process = ['Warszawa']
        print(f"Using default city: Warszawa")
    
    if not cities_to_process:
        print("Error: No cities to process")
        sys.exit(1)
    
    print("=== KEBAB RANK HISTORICAL DATA GENERATOR ===")
    print(f"Cities to process: {len(cities_to_process)}")
    print(f"Days ago: {args.days_ago}")
    print(f"Preview mode: {args.preview}")
    print(f"Apply changes: {args.apply}")
    print(f"Batch delay: {args.batch_delay} seconds")
    print()
    
    if args.backup and args.apply:
        print("Creating backup...")
        if not generator.backup_current_data():
            print("Backup failed. Aborting.")
            sys.exit(1)
    
    # Process each city
    results = []
    successful_cities = []
    failed_cities = []
    
    for i, city_name in enumerate(cities_to_process):
        print(f"\n{'='*60}")
        print(f"PROCESSING CITY {i+1}/{len(cities_to_process)}: {city_name.upper()}")
        print(f"{'='*60}")
        
        try:
            # Generate historical data for this city
            result = generator.generate_realistic_historical_data(
                city_name, 
                args.days_ago, 
                preview_only=(not args.apply)
            )
            
            if "error" in result:
                print(f"❌ Error processing {city_name}: {result['error']}")
                failed_cities.append((city_name, result['error']))
                continue
            
            # Display results for this city
            print(f"\n=== RESULTS FOR {result['city'].upper()} ===")
            print(f"Historical date: {result['historical_date']}")
            print(f"Total kebabs: {result['total_kebabs']}")
            print(f"Historical data entries: {result['historical_data_count']}")
            print(f"New entries: {result['changes']['new_entries']}")
            print(f"No change: {result['changes']['no_change']}")
            print(f"Small changes: {result['changes']['small_change']}")
            print(f"Moderate changes: {result['changes']['moderate_change']}")
            
            print(f"\n=== SAMPLE CHANGES ===")
            for j, change in enumerate(result['preview'][:5]):  # Show first 5
                # Handle "NEW" entries properly
                hist_rank = change['historical_rank']
                if hist_rank == "NEW":
                    hist_rank_display = "NEW"
                else:
                    hist_rank_display = f"{hist_rank:2d}"
                
                print(f"{j+1:2d}. {change['name'][:30]:30} | Rank: {hist_rank_display} → {change['current_rank']:2d} | Change: {change['change']:>4}")
            
            if args.apply:
                print(f"\n✓ Applied {result.get('inserted_count', 0)} historical records for {city_name}")
                
                if args.validate:
                    print("\n=== VALIDATION ===")
                    validation = generator.validate_historical_data(city_name)
                    if "error" in validation:
                        print(f"Validation error: {validation['error']}")
                    else:
                        print(f"Validated {validation['total_rankings']} rankings")
                        print(f"Rankings with changes: {validation['rankings_with_changes']}")
                        print(f"New entries: {validation['new_entries']}")
                        print(f"Stable entries: {validation['stable_entries']}")
            
            results.append(result)
            successful_cities.append(city_name)
            
            # Add delay between cities (except for the last one)
            if i < len(cities_to_process) - 1 and args.batch_delay > 0:
                print(f"\nWaiting {args.batch_delay} seconds before next city...")
                import time
                time.sleep(args.batch_delay)
                
        except Exception as e:
            print(f"❌ Unexpected error processing {city_name}: {e}")
            import traceback
            traceback.print_exc()
            failed_cities.append((city_name, str(e)))
            continue
    
    # Display final summary
    print(f"\n{'='*60}")
    print("=== PROCESSING SUMMARY ===")
    print(f"{'='*60}")
    print(f"Total cities processed: {len(cities_to_process)}")
    print(f"✅ Successful: {len(successful_cities)}")
    print(f"❌ Failed: {len(failed_cities)}")
    
    if successful_cities:
        print(f"\n✅ Successful cities: {', '.join(successful_cities)}")
    
    if failed_cities:
        print(f"\n❌ Failed cities:")
        for city, error in failed_cities:
            print(f"  - {city}: {error}")
    
    # Calculate totals
    total_kebabs = sum(result['total_kebabs'] for result in results)
    total_entries = sum(result['historical_data_count'] for result in results)
    
    print(f"\n📊 TOTAL STATISTICS:")
    print(f"Total kebabs across all cities: {total_kebabs}")
    print(f"Total historical entries created: {total_entries}")
    
    if args.preview and not args.apply:
        print(f"\n💡 This was a preview. To apply changes, run with --apply flag")
        print(f"   Example: python {sys.argv[0]} --all-cities --apply --backup")


if __name__ == "__main__":
    main()
