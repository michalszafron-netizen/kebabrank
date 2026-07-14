# fix_single_city.py - Fix rankings for a single city
import os
import sys
from dotenv import load_dotenv
from services.database import DatabaseService
from services.ranking import RankingService

load_dotenv()

def fix_city_rankings(city_name):
    """Recalculate and fix rankings for a single city"""
    print(f"🔧 Starting ranking fix process for {city_name}...")
    
    # Initialize services
    db_service = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    ranking_service = RankingService()
    
    # Get city ID
    city_id = db_service.get_city_id(city_name)
    if not city_id:
        print(f"✗ City '{city_name}' not found in database")
        return
    print(f"\n📍 Fixing rankings for {city_name} (ID: {city_id})...")
    
    try:
        # Get all kebab places in the city with their latest ratings
        response = db_service.client.table('kebab_places').select(
            'id, name, ratings_history!inner(*)'
        ).eq('city_id', city_id).execute()
        
        # Get latest ratings for each place
        latest_ratings = []
        for place in response.data:
            if place['ratings_history']:
                # Sort by date to get the most recent
                sorted_ratings = sorted(place['ratings_history'], 
                                      key=lambda x: x['data_fetched_at'], 
                                      reverse=True)
                if sorted_ratings:
                    latest_rating = sorted_ratings[0]
                    latest_rating['place_name'] = place['name']
                    latest_rating['place_id'] = place['id']
                    latest_ratings.append(latest_rating)
        
        if not latest_ratings:
            print(f"  No kebabs found in {city_name}")
            return
        
        # Calculate rank scores if missing
        for rating in latest_ratings:
            if not rating.get('rank_score') or rating['rank_score'] == 0:
                rating['rank_score'] = ranking_service.calculate_rank_score(
                    rating['rating'],
                    rating['total_reviews'],
                    rating.get('positive_percentage', 0)
                )
        
        # Sort by rank_score (descending), then by total_reviews (descending)
        sorted_ratings = sorted(latest_ratings, 
                              key=lambda x: (x['rank_score'], x['total_reviews']), 
                              reverse=True)
        
        # Update rankings in database
        for i, rating in enumerate(sorted_ratings):
            new_rank = i + 1
            old_rank = rating.get('city_rank', 0)
            
            # Update in database
            db_service.client.table('ratings_history').update({
                'city_rank': new_rank,
                'rank_score': rating['rank_score']  # Update score too if it was recalculated
            }).eq('id', rating['id']).execute()
            
            # Show what changed
            if old_rank != new_rank:
                print(f"  ✓ {rating['place_name']}: #{old_rank} → #{new_rank} (Score: {rating['rank_score']})")
            else:
                print(f"  - {rating['place_name']}: #{new_rank} unchanged (Score: {rating['rank_score']})")
        
        print(f"\n✅ Fixed {len(sorted_ratings)} kebabs in {city_name}")

    except Exception as e:
        print(f"  ✗ Error fixing {city_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_single_city.py [city_name]")
        sys.exit(1)
    
    city_name = sys.argv[1]
    fix_city_rankings(city_name)
