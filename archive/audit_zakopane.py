import os
from pocketbase import PocketBase
from dotenv import load_dotenv

def audit_zakopane():
    load_dotenv()
    pb = PocketBase(os.getenv('PB_URL'))
    
    # 1. Get Zakopane ID
    city = pb.collection('cities').get_first_list_item('name="Zakopane"')
    city_id = city.id
    print(f"Zakopane ID: {city_id}")
    
    # 2. Get all kebab places in Zakopane
    places = pb.collection('kebab_places').get_full_list(query_params={'filter': f'city="{city_id}"'})
    print(f"Total places in DB for Zakopane: {len(places)}")
    
    # 3. Get all ratings for Zakopane
    ratings = pb.collection('ratings').get_full_list(
        query_params={
            'filter': f'kebab_place.city="{city_id}"',
            'sort': '-created',
            'expand': 'kebab_place'
        }
    )
    
    if not ratings:
        print("No ratings found.")
        return
        
    # Group by created (batches)
    batches = {}
    for r in ratings:
        ts = r.created[:16] # Group by minute for safety
        if ts not in batches: batches[ts] = []
        batches[ts].append(r)
        
    sorted_ts = sorted(batches.keys(), reverse=True)
    print(f"Found {len(sorted_ts)} batches.")
    
    for i, ts in enumerate(sorted_ts):
        batch = batches[ts]
        print(f"Batch {i} ({ts}): {len(batch)} ratings")
        if i == 0:
            # Check names of latest batch
            names = [getattr(r, 'expand', {}).get('kebab_place', {}).name for r in batch]
            print(f"  Sample names: {', '.join(names[:5])}")
    
    # Check for duplicates or ID issues
    id_counts = {}
    for p in places:
        g_id = p.google_place_id
        id_counts[g_id] = id_counts.get(g_id, 0) + 1
        
    duplicates = {k: v for k, v in id_counts.items() if v > 1}
    if duplicates:
        print(f"DUPLICATES FOUND: {duplicates}")
    else:
        print("No duplicate Google Place IDs found.")

if __name__ == "__main__":
    audit_zakopane()
