import os
import sys
import io
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def audit_missing():
    load_dotenv()
    pb = PocketbaseService(os.getenv('PB_URL'))
    
    city_id = pb.get_city_id("Zakopane")
    
    ratings = pb.client.collection('ratings').get_full_list(
        query_params={
            'filter': f'kebab_place.city="{city_id}"',
            'sort': '-created',
            'expand': 'kebab_place'
        }
    )
    
    from datetime import datetime, timedelta
    batches = []
    current_batch = []
    last_time = None
    for r in ratings:
        if last_time is None or (last_time - r.created) < timedelta(minutes=60):
            current_batch.append(r)
        else:
            batches.append(current_batch)
            current_batch = [r]
        last_time = r.created
    if current_batch: batches.append(current_batch)
    
    current_batch = batches[0]
    prev_batch = batches[1]
    
    current_ids = {getattr(r, 'expand', {}).get('kebab_place', {}).google_place_id for r in current_batch}
    prev_data = {} # id -> name
    for r in prev_batch:
        p = getattr(r, 'expand', {}).get('kebab_place', {})
        if p: prev_data[p.google_place_id] = p.name
        
    print(f"Places in Prev Batch ({len(prev_data)} unique IDs):")
    for g_id, name in prev_data.items():
        status = "MATCHED" if g_id in current_ids else "MISSING"
        print(f"  {status}: {name} ({g_id})")

if __name__ == "__main__":
    audit_missing()
