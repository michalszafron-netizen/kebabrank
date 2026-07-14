import os
import sys
import io
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def audit_zakopane():
    load_dotenv()
    pb = PocketbaseService(os.getenv('PB_URL'))
    
    city_name = "Zakopane"
    city_id = pb.get_city_id(city_name)
    print(f"Zakopane ID: {city_id}")
    
    # 1. Get all kebab places
    places = pb.client.collection('kebab_places').get_full_list(query_params={'filter': f'city="{city_id}"'})
    print(f"Total places in DB for Zakopane: {len(places)}")
    
    # 2. Get all ratings
    ratings = pb.client.collection('ratings').get_full_list(
        query_params={
            'filter': f'kebab_place.city="{city_id}"',
            'sort': '-created',
            'expand': 'kebab_place'
        }
    )
    
    print(f"Total ratings found: {len(ratings)}")
    
    # 3. Identify batches by created time
    from datetime import datetime, timedelta
    
    if not ratings:
        print("No ratings found.")
        return
        
    batches = []
    current_batch = []
    last_time = None
    
    for r in ratings:
        # Group records within 60 minutes of each other
        if last_time is None or (last_time - r.created) < timedelta(minutes=60):
            current_batch.append(r)
        else:
            batches.append(current_batch)
            current_batch = [r]
        last_time = r.created
    
    if current_batch:
        batches.append(current_batch)
        
    print(f"Detected {len(batches)} batches.")
    
    for i, batch in enumerate(batches):
        ts = batch[0].created
        print(f"Batch {i} ({ts}): {len(batch)} places")
        
        # Collect IDs and Names
        data = []
        for r in batch:
            p = getattr(r, 'expand', {}).get('kebab_place', {})
            data.append({
                'name': p.name if p else "N/A",
                'g_id': p.google_place_id if p else "N/A",
                'rank': getattr(r, 'city_rank', 0)
            })
        
        # Print top 5
        data.sort(key=lambda x: x['rank'])
        for item in data[:5]:
            print(f"  #{item['rank']} {item['name']} ({item['g_id']})")
        
        if i == 0:
            latest_ids = {item['g_id'] for item in data}
        elif i == 1:
            prev_ids = {item['g_id'] for item in data}
            matches = latest_ids.intersection(prev_ids)
            print(f"  Matches with previous batch: {len(matches)}")
            missing = prev_ids - latest_ids
            if missing:
                print(f"  Places from prev batch NOT in current: {len(missing)}")
            new_places = latest_ids - prev_ids
            print(f"  Places marked as NEW in current: {len(new_places)}")

if __name__ == "__main__":
    audit_zakopane()
