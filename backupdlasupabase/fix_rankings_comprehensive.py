# fix_rankings_comprehensive.py - Comprehensive fix for kebab rankings
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from services.database import DatabaseService
from services.ranking import RankingService

load_dotenv()

class RankingFixer:
    def __init__(self):
        self.db_service = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
        self.ranking_service = RankingService()
    
    def fix_all_rankings(self):
        """Fix rankings for all cities"""
        print("🔧 Starting comprehensive ranking fix...")
        print("=" * 60)
        
        cities = self.db_service.get_cities()
        total_fixed = 0
        
        for city in cities:
            fixed_count = self.fix_city_rankings(city['name'], city['id'])
            total_fixed += fixed_count
        
        print(f"\n✅ Fixed rankings for {total_fixed} kebabs across {len(cities)} cities!")
        return total_fixed
    
    def fix_city_rankings(self, city_name: str, city_id: int):
        """Fix rankings for a single city"""
        print(f"\n📍 Processing: {city_name}")
        print("-" * 40)
        
        try:
            # Get all kebab places with their LATEST ratings
            kebabs_data = self._get_latest_kebab_data(city_id)
            
            if not kebabs_data:
                print(f"  ⚠️ No kebabs found in {city_name}")
                return 0
            
            # Calculate rank scores if missing
            for kebab in kebabs_data:
                if not kebab.get('rank_score') or kebab['rank_score'] == 0:
                    kebab['rank_score'] = self.ranking_service.calculate_rank_score(
                        kebab['rating'],
                        kebab['total_reviews'],
                        kebab.get('positive_percentage', 0)
                    )
                    print(f"  📊 Calculated rank_score for {kebab['name']}: {kebab['rank_score']}")
            
            # Sort by rank_score (DESC), then by total_reviews (DESC)
            sorted_kebabs = sorted(
                kebabs_data,
                key=lambda x: (x['rank_score'], x['total_reviews']),
                reverse=True
            )
            
            # Update rankings in database
            updated_count = 0
            for new_rank, kebab in enumerate(sorted_kebabs, 1):
                old_rank = kebab.get('city_rank', 0)
                
                # Update the rating history record
                update_data = {
                    'city_rank': new_rank,
                    'rank_score': kebab['rank_score']
                }
                
                self.db_service.client.table('ratings_history').update(
                    update_data
                ).eq('id', kebab['rating_id']).execute()
                
                # Display changes
                if old_rank != new_rank:
                    print(f"  ✓ {kebab['name']}: #{old_rank} → #{new_rank} (Score: {kebab['rank_score']:.2f})")
                    updated_count += 1
                else:
                    print(f"  - {kebab['name']}: #{new_rank} unchanged (Score: {kebab['rank_score']:.2f})")
            
            print(f"  📈 Updated {updated_count} rankings in {city_name}")
            return len(sorted_kebabs)
            
        except Exception as e:
            print(f"  ❌ Error fixing {city_name}: {e}")
            import traceback
            traceback.print_exc()
            return 0
    
    def _get_latest_kebab_data(self, city_id: int):
        """Get the latest rating data for all kebabs in a city"""
        try:
            # First, get all kebab places in the city
            places_response = self.db_service.client.table('kebab_places').select(
                'id, name, google_place_id'
            ).eq('city_id', city_id).execute()
            
            if not places_response.data:
                return []
            
            latest_kebabs = []
            
            # For each place, get its latest rating
            for place in places_response.data:
                # Get the most recent rating for this kebab
                rating_response = self.db_service.client.table('ratings_history').select(
                    '*'
                ).eq('kebab_place_id', place['id']).order(
                    'data_fetched_at', desc=True
                ).limit(1).execute()
                
                if rating_response.data:
                    rating = rating_response.data[0]
                    latest_kebabs.append({
                        'rating_id': rating['id'],
                        'place_id': place['id'],
                        'google_place_id': place['google_place_id'],
                        'name': place['name'],
                        'rating': rating['rating'],
                        'total_reviews': rating['total_reviews'],
                        'positive_percentage': rating.get('positive_percentage', 0),
                        'rank_score': rating.get('rank_score', 0),
                        'city_rank': rating.get('city_rank', 0),
                        'data_fetched_at': rating['data_fetched_at']
                    })
            
            return latest_kebabs
            
        except Exception as e:
            print(f"Error getting kebab data: {e}")
            return []
    
    def verify_rankings(self, city_name: str):
        """Verify that rankings are correct for a city"""
        print(f"\n🔍 Verifying rankings for {city_name}...")
        
        rankings = self.db_service.get_city_rankings(city_name)
        
        if not rankings:
            print("  ⚠️ No rankings found")
            return False
        
        print(f"\n  Top 10 kebabs in {city_name}:")
        print("  " + "-" * 60)
        print(f"  {'Rank':<6} {'Name':<30} {'Score':<8} {'Rating':<8} {'Reviews':<8}")
        print("  " + "-" * 60)
        
        is_valid = True
        prev_score = float('inf')
        
        for i, kebab in enumerate(rankings[:40]):
            rank = kebab.get('city_rank', i + 1)
            score = kebab['rank_score']
            
            # Check if ordering is correct
            if score > prev_score:
                is_valid = False
                status = "❌"
            else:
                status = "✅"
            
            print(f"  {status} #{rank:<4} {kebab['name'][:28]:<30} {score:<8.2f} {kebab['rating']:<8.1f} {kebab['total_reviews']:<8}")
            
            prev_score = score
        
        if is_valid:
            print("\n  ✅ Rankings are correctly ordered!")
        else:
            print("\n  ❌ Rankings have ordering issues!")
        
        return is_valid

def main():
    """Main function with menu"""
    fixer = RankingFixer()
    
    if len(sys.argv) > 1:
        # Command line argument provided
        if sys.argv[1] == '--all':
            fixer.fix_all_rankings()
        elif sys.argv[1] == '--verify':
            if len(sys.argv) > 2:
                fixer.verify_rankings(sys.argv[2])
            else:
                print("Please specify a city name to verify")
        else:
            # Fix specific city
            city_name = ' '.join(sys.argv[1:])
            city_id = fixer.db_service.get_city_id(city_name)
            if city_id:
                fixer.fix_city_rankings(city_name, city_id)
                fixer.verify_rankings(city_name)
            else:
                print(f"City '{city_name}' not found!")
    else:
        # Interactive menu
        print("\n🥙 KebabRank - Ranking Fixer")
        print("=" * 40)
        print("1. Fix rankings for all cities")
        print("2. Fix rankings for specific city")
        print("3. Verify rankings for a city")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ")
        
        if choice == '1':
            fixer.fix_all_rankings()
        elif choice == '2':
            city_name = input("Enter city name: ")
            city_id = fixer.db_service.get_city_id(city_name)
            if city_id:
                fixer.fix_city_rankings(city_name, city_id)
                fixer.verify_rankings(city_name)
            else:
                print(f"City '{city_name}' not found!")
        elif choice == '3':
            city_name = input("Enter city name to verify: ")
            fixer.verify_rankings(city_name)
        elif choice == '4':
            print("Goodbye!")
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()