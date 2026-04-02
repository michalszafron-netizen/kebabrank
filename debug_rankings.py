import os
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

load_dotenv()

db = PocketbaseService(os.getenv('PB_URL'), os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))
db._ensure_auth()

def debug_rankings(city_name):
    print(f"--- Debugging {city_name} ---")
    city_id = db.get_city_id(city_name)
    print(f"City ID: {city_id}")
    
    if not city_id:
        # Try finding city by name approx
        cities = db.get_cities()
        print(f"Available cities: {[c['name'] for c in cities[:5]]}...")
        return

    # 1. Latest rating for city
    res = db.client.collection('ratings').get_list(
        1, 1,
        query_params={
            "filter": f'kebab_place.city="{city_id}"',
            "sort": "-created"
        }
    )
    print(f"Latest ratings found: {res.total_items}")
    if res.items:
        print(f"Latest timestamp: {res.items[0].created}")
        
        # 2. Try the full query logic
        rankings = db.get_city_rankings(city_name, limit=5)
        print(f"Rankings returned: {len(rankings)}")
        if rankings:
            print(f"First rank: {rankings[0]['name']} - Score {rankings[0]['rank_score']}")

if __name__ == "__main__":
    debug_rankings("Kraków")
    debug_rankings("Warszawa")
