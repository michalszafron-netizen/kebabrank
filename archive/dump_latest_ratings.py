import os
import io
import sys
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def dump_latest_ratings():
    load_dotenv()
    pb = PocketbaseService(os.getenv('PB_URL'))
    
    city_name = "Zakopane"
    city_id = pb.get_city_id(city_name)
    
    # Get latest ratings
    ratings = pb.client.collection('ratings').get_full_list(
        query_params={
            'filter': f'kebab_place.city="{city_id}"',
            'sort': '-created',
            'expand': 'kebab_place'
        }
    )
    
    if not ratings:
        print("No ratings found.")
        return
        
    latest_time = ratings[0].created
    window_start = latest_time - timedelta(minutes=60)
    
    batch = [r for r in ratings if r.created >= window_start]
    
    print(f"--- Latest Batch Ratings for {city_name} (Time: {latest_time}) ---")
    print(f"Items in batch: {len(batch)}")
    
    # Sort by city_rank
    batch.sort(key=lambda x: getattr(x, 'city_rank', 999))
    
    for r in batch:
        p = getattr(r, 'expand', {}).get('kebab_place', {})
        name = p.name if p else "Unknown"
        print(f"City Rank: {getattr(r, 'city_rank', 'N/A')} | Score: {r.rank_score} | Name: {name}")

if __name__ == "__main__":
    dump_latest_ratings()
