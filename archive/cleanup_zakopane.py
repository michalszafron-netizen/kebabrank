import os
import sys
import io
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def cleanup_zakopane():
    load_dotenv()
    pb = PocketbaseService(os.getenv('PB_URL'))
    
    city_id = pb.get_city_id("Zakopane")
    print(f"Cleaning up Zakopane (ID: {city_id})...")
    
    # 1. Get ALL ratings for Zakopane
    ratings = pb.client.collection('ratings').get_full_list(
        query_params={
            'filter': f'kebab_place.city="{city_id}"',
            'sort': '-created',
        }
    )
    
    print(f"Total ratings found: {len(ratings)}")
    
    # 2. Group by (place_id, hour) to keep only the latest one per hour
    seen = set()
    to_delete = []
    
    for r in ratings:
        # Key: place + timestamp grouped by minute string
        ts_minute = r.created.strftime('%Y-%m-%d %H:%M')
        key = (r.kebab_place, ts_minute)
        
        if key in seen:
            to_delete.append(r.id)
        else:
            seen.add(key)
            
    print(f"Found {len(to_delete)} duplicate ratings to delete.")
    
    count = 0
    for rid in to_delete:
        try:
            pb.client.collection('ratings').delete(rid)
            count += 1
            if count % 50 == 0: print(f"Deleted {count}...")
        except Exception as e:
            print(f"Error deleting {rid}: {e}")
            
    print(f"✓ Deleted {count} duplicates.")

if __name__ == "__main__":
    cleanup_zakopane()
