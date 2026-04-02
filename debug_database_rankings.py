# debug_database_rankings.py - Debug what's actually in the database
import os
from dotenv import load_dotenv
from services.database import DatabaseService
from datetime import datetime

load_dotenv()

def debug_rankings(city_name: str):
    """Debug rankings directly from database"""
    db = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    
    print(f"\n🔍 Debugging rankings for {city_name}")
    print("=" * 80)
    
    # Get city ID
    city_id = db.get_city_id(city_name)
    if not city_id:
        print(f"❌ City '{city_name}' not found!")
        return
    
    print(f"✅ City ID: {city_id}")
    
    # Method 1: What get_city_rankings returns
    print("\n📊 Method 1: get_city_rankings() output:")
    print("-" * 80)
    rankings = db.get_city_rankings(city_name)
    
    if rankings:
        print(f"{'Rank':<6} {'Name':<30} {'Score':<10} {'Rating':<8} {'Reviews':<10} {'City Rank':<10}")
        print("-" * 80)
        for i, kebab in enumerate(rankings[:10]):
            print(f"{i+1:<6} {kebab['name'][:28]:<30} {kebab['rank_score']:<10.2f} "
                  f"{kebab['rating']:<8.1f} {kebab['total_reviews']:<10} {kebab.get('city_rank', 'N/A'):<10}")
    else:
        print("❌ No rankings returned!")
    
    # Method 2: Direct database query
    print("\n📊 Method 2: Direct database query:")
    print("-" * 80)
    
    # Get all kebab places in the city
    places = db.client.table('kebab_places').select(
        'id, name, google_place_id'
    ).eq('city_id', city_id).execute()
    
    if places.data:
        print(f"Found {len(places.data)} kebab places in {city_name}")
        
        # For each place, get its latest rating
        all_ratings = []
        for place in places.data:
            ratings = db.client.table('ratings_history').select(
                'id, rating, total_reviews, rank_score, city_rank, data_fetched_at'
            ).eq('kebab_place_id', place['id']).order(
                'data_fetched_at', desc=True
            ).limit(1).execute()
            
            if ratings.data:
                rating = ratings.data[0]
                all_ratings.append({
                    'name': place['name'],
                    'rating': rating['rating'],
                    'total_reviews': rating['total_reviews'],
                    'rank_score': rating['rank_score'],
                    'city_rank': rating['city_rank'],
                    'rating_id': rating['id'],
                    'fetched_at': rating['data_fetched_at']
                })
        
        # Sort by rank_score to see what order they should be in
        all_ratings.sort(key=lambda x: (x['rank_score'], x['total_reviews']), reverse=True)
        
        print(f"\n{'Should Be':<10} {'DB Says':<10} {'Name':<30} {'Score':<10} {'Rating':<8} {'Reviews':<10}")
        print("-" * 90)
        for i, kebab in enumerate(all_ratings[:10]):
            should_be = i + 1
            db_says = kebab['city_rank']
            match = "✅" if should_be == db_says else "❌"
            print(f"{match} {should_be:<8} {db_says:<10} {kebab['name'][:28]:<30} "
                  f"{kebab['rank_score']:<10.2f} {kebab['rating']:<8.1f} {kebab['total_reviews']:<10}")
        
        # Show fetch times
        print(f"\n📅 Latest data fetch times:")
        for kebab in all_ratings[:3]:
            print(f"  - {kebab['name']}: {kebab['fetched_at']}")
    
    # Method 3: Check for duplicate entries
    print("\n🔍 Checking for duplicate entries:")
    print("-" * 80)
    
    for place in places.data[:5]:  # Check first 5 places
        ratings_count = db.client.table('ratings_history').select(
            'id, data_fetched_at, rank_score, city_rank'
        ).eq('kebab_place_id', place['id']).order(
            'data_fetched_at', desc=True
        ).limit(5).execute()
        
        if len(ratings_count.data) > 1:
            print(f"\n{place['name']} has {len(ratings_count.data)} rating entries:")
            for r in ratings_count.data[:3]:
                print(f"  - ID: {r['id']}, Score: {r['rank_score']}, Rank: {r['city_rank']}, Date: {r['data_fetched_at']}")

if __name__ == "__main__":
    import sys
    city = sys.argv[1] if len(sys.argv) > 1 else "Kraków"
    debug_rankings(city)