# fix_and_verify_rankings.py - Complete fix for ranking issues
import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv
from services.database import DatabaseService
from services.ranking import RankingService

load_dotenv()

class CompleteFix:
    def __init__(self):
        self.db = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
        self.ranking_service = RankingService()
    
    def fix_city_complete(self, city_name: str):
        """Complete fix for a city's rankings"""
        print(f"\n🔧 Complete Fix for {city_name}")
        print("=" * 80)
        
        city_id = self.db.get_city_id(city_name)
        if not city_id:
            print(f"❌ City '{city_name}' not found!")
            return False
        
        # Step 1: Get all places in the city
        places = self.db.client.table('kebab_places').select(
            'id, name, google_place_id'
        ).eq('city_id', city_id).execute()
        
        if not places.data:
            print("❌ No kebab places found!")
            return False
        
        print(f"✅ Found {len(places.data)} kebab places")
        
        # Step 2: Get latest rating for each place and calculate scores
        latest_ratings = []
        
        for place in places.data:
            # Get the most recent rating
            rating_result = self.db.client.table('ratings_history').select(
                '*'
            ).eq('kebab_place_id', place['id']).order(
                'data_fetched_at', desc=True
            ).limit(1).execute()
            
            if rating_result.data:
                rating = rating_result.data[0]
                
                # Calculate rank_score if missing
                if not rating.get('rank_score') or rating['rank_score'] == 0:
                    rating['rank_score'] = self.ranking_service.calculate_rank_score(
                        rating['rating'],
                        rating['total_reviews'],
                        rating.get('positive_percentage', 0)
                    )
                    print(f"  📊 Calculated score for {place['name']}: {rating['rank_score']:.2f}")
                
                latest_ratings.append({
                    'rating_id': rating['id'],
                    'place_id': place['id'],
                    'place_name': place['name'],
                    'google_place_id': place['google_place_id'],
                    'rating': rating['rating'],
                    'total_reviews': rating['total_reviews'],
                    'rank_score': rating['rank_score'],
                    'old_city_rank': rating.get('city_rank', 0)
                })
        
        # Step 3: Sort by rank_score (desc), then total_reviews (desc)
        latest_ratings.sort(
            key=lambda x: (x['rank_score'], x['total_reviews']),
            reverse=True
        )
        
        # Step 4: Update database with correct rankings and scores
        print("\n📝 Updating database...")
        updates_made = 0
        
        for new_rank, kebab in enumerate(latest_ratings, 1):
            # Update the database
            update_data = {
                'city_rank': new_rank,
                'rank_score': kebab['rank_score']
            }
            
            try:
                self.db.client.table('ratings_history').update(
                    update_data
                ).eq('id', kebab['rating_id']).execute()
                
                if kebab['old_city_rank'] != new_rank:
                    print(f"  ✅ {kebab['place_name']}: #{kebab['old_city_rank']} → #{new_rank} "
                          f"(Score: {kebab['rank_score']:.2f})")
                    updates_made += 1
                else:
                    print(f"  - {kebab['place_name']}: #{new_rank} unchanged "
                          f"(Score: {kebab['rank_score']:.2f})")
                    
            except Exception as e:
                print(f"  ❌ Error updating {kebab['place_name']}: {e}")
        
        print(f"\n✅ Updated {updates_made} rankings")
        
        # Step 5: Verify the fix
        print("\n🔍 Verifying fix...")
        time.sleep(1)  # Give database time to update
        
        # Get fresh data using the same method as the web app
        web_rankings = self.db.get_city_rankings(city_name)
        
        if web_rankings:
            print(f"\n📊 Top 10 as the web app will see them:")
            print("-" * 80)
            print(f"{'Rank':<6} {'Name':<30} {'Score':<10} {'Rating':<8} {'Reviews':<10}")
            print("-" * 80)
            
            all_correct = True
            for i, kebab in enumerate(web_rankings[:10]):
                expected_rank = i + 1
                displayed_rank = kebab.get('city_rank', expected_rank)
                
                if expected_rank != displayed_rank:
                    all_correct = False
                    status = "❌"
                else:
                    status = "✅"
                
                print(f"{status} #{displayed_rank:<4} {kebab['name'][:28]:<30} "
                      f"{kebab['rank_score']:<10.2f} {kebab['rating']:<8.1f} "
                      f"{kebab['total_reviews']:<10}")
            
            if all_correct:
                print("\n✅ All rankings are now correct!")
            else:
                print("\n⚠️ Some rankings still have issues!")
        
        return True
    
    def test_web_endpoint(self, city_name: str):
        """Test what the web API returns"""
        print(f"\n🌐 Testing web API endpoint for {city_name}...")
        
        try:
            import requests
            response = requests.get(f'http://localhost:5000/api/rankings/{city_name}')
            
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    rankings = data['data']
                    print(f"✅ API returned {len(rankings)} kebabs")
                    
                    # Check order
                    print("\nAPI Response Order:")
                    for i, kebab in enumerate(rankings[:5]):
                        print(f"  {i+1}. {kebab['name']} - Score: {kebab['rank_score']}")
                else:
                    print(f"❌ API error: {data.get('message', 'Unknown error')}")
            else:
                print(f"❌ HTTP error: {response.status_code}")
        except Exception as e:
            print(f"❌ Could not connect to API: {e}")
            print("   Make sure Flask app is running!")

def main():
    fixer = CompleteFix()
    
    if len(sys.argv) > 1:
        city_name = ' '.join(sys.argv[1:])
    else:
        city_name = "Kraków"
    
    # Fix the rankings
    if fixer.fix_city_complete(city_name):
        # Test the API
        fixer.test_web_endpoint(city_name)
        
        print("\n💡 Next steps:")
        print("1. If Flask is running, refresh your browser (Ctrl+F5 for hard refresh)")
        print("2. If rankings still wrong, restart Flask:")
        print("   - Stop Flask (Ctrl+C)")
        print("   - Run: python app.py")
        print("3. Check http://localhost:5000 and search for", city_name)

if __name__ == "__main__":
    main()