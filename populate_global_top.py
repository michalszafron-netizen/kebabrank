"""
Script to create the global_top collection in PocketBase and populate it
with pre-computed global rankings. Run this after data updates.
"""
import sys, io, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from dotenv import load_dotenv
load_dotenv()

from services.pocketbase_db import PocketbaseService

PB_URL = os.getenv('PB_URL')
PB_EMAIL = os.getenv('PB_EMAIL')
PB_PASSWORD = os.getenv('PB_PASSWORD')

def create_global_top_collection():
    """Create the global_top collection in PocketBase via the Admin API."""
    import requests
    
    # Authenticate as admin
    auth_resp = requests.post(f"{PB_URL}/api/collections/_superusers/auth-with-password", json={
        "identity": PB_EMAIL,
        "password": PB_PASSWORD
    })
    token = auth_resp.json().get("token")
    if not token:
        print(f"Auth failed: {auth_resp.json()}")
        return False
    
    headers = {"Authorization": token}
    
    # Check if collection already exists
    check = requests.get(f"{PB_URL}/api/collections/global_top", headers=headers)
    if check.status_code == 200:
        print("global_top collection already exists!")
        return True
    
    # Create the collection
    collection_schema = {
        "name": "global_top",
        "type": "base",
        "fields": [
            {"name": "name", "type": "text", "required": True},
            {"name": "address", "type": "text"},
            {"name": "city", "type": "text"},
            {"name": "google_place_id", "type": "text"},
            {"name": "place_id", "type": "text"},
            {"name": "lat", "type": "number"},
            {"name": "lng", "type": "number"},
            {"name": "photo_url", "type": "text"},
            {"name": "rating", "type": "number"},
            {"name": "total_reviews", "type": "number"},
            {"name": "rank_score", "type": "number"},
            {"name": "ai_score", "type": "number"},
            {"name": "has_ai_analysis", "type": "bool"},
            {"name": "global_rank", "type": "number"},
            {"name": "rank_change", "type": "number"},
            {"name": "rank_change_indicator", "type": "text"},
            {"name": "is_new", "type": "bool"},
            {"name": "opening_hours", "type": "json"}
        ]
    }
    
    resp = requests.post(f"{PB_URL}/api/collections", json=collection_schema, headers=headers)
    if resp.status_code in [200, 201]:
        print("✅ global_top collection created!")
        return True
    else:
        print(f"❌ Failed to create collection: {resp.status_code} - {resp.text}")
        return False


def populate_global_top():
    """Populate global_top by iterating all cities and computing true rankings.
    This is the SLOW but ACCURATE approach — run during data updates only.
    """
    db = PocketbaseService(PB_URL, PB_EMAIL, PB_PASSWORD)
    
    print("Fetching city rankings for all cities...")
    cities = db.get_cities()
    
    all_rankings = []
    for city_info in cities:
        city_name = city_info.get('name')
        if not city_name:
            continue
        try:
            rankings = db.get_city_rankings(city_name, limit=50) # Increased from 10 to 50
            for r in rankings:
                r['city'] = city_name
            all_rankings.extend(rankings)
            print(f"  {city_name}: {len(rankings)} rankings")
        except Exception as e:
            print(f"  {city_name}: ERROR - {e}")
    
    # Deduplicate by google_place_id (keep highest score)
    best_per_place = {}
    for r in all_rankings:
        g_id = r.get('google_place_id', '')
        if not g_id:
            continue
        # If we see the same place multiple times, keep the highest score
        if g_id not in best_per_place or r.get('rank_score', 0) > best_per_place[g_id].get('rank_score', 0):
            best_per_place[g_id] = r
    
    # Sort by rank_score descending, take top 50
    sorted_rankings = sorted(
        best_per_place.values(),
        key=lambda x: (x.get('rank_score', 0), x.get('total_reviews', 0)),
        reverse=True
    )[:50]
    
    # --- Trend Calculation ---
    print("\nCalculating trends (comparing with existing global_top)...")
    import requests
    auth_resp = requests.post(f"{PB_URL}/api/collections/_superusers/auth-with-password", json={
        "identity": PB_EMAIL,
        "password": PB_PASSWORD
    })
    token = auth_resp.json().get("token")
    headers = {"Authorization": token}
    
    # Fetch existing rankings to compare
    old_rankings_map = {} # google_place_id -> global_rank
    existing_resp = requests.get(f"{PB_URL}/api/collections/global_top/records?perPage=200", headers=headers)
    if existing_resp.status_code == 200:
        items = existing_resp.json().get("items", [])
        for item in items:
            g_id = item.get('google_place_id')
            if g_id:
                old_rankings_map[g_id] = item.get('global_rank')
    
    # Apply trends to new rankings
    for i, r in enumerate(sorted_rankings):
        new_rank = i + 1
        r['global_rank'] = new_rank
        g_id = r.get('google_place_id')
        
        if g_id in old_rankings_map:
            old_rank = old_rankings_map[g_id]
            change = old_rank - new_rank # e.g. #5 to #3 = +2
            r['rank_change'] = change
            if change > 0:
                r['rank_change_indicator'] = 'up'
            elif change < 0:
                r['rank_change_indicator'] = 'down'
            else:
                r['rank_change_indicator'] = 'neutral'
            r['is_new'] = False
        else:
            # Not in previous Top 50
            r['rank_change'] = 0
            r['rank_change_indicator'] = 'neutral'
            r['is_new'] = True if old_rankings_map else False # Only mark as NEW if we actually HAD a previous list
    
    print(f"Computed {len(sorted_rankings)} global rankings with trends. Clearing old data...")
    
    # Delete all existing records (loop until empty)
    while True:
        existing = requests.get(f"{PB_URL}/api/collections/global_top/records?perPage=200", headers=headers)
        if existing.status_code == 200:
            items = existing.json().get("items", [])
            if not items:
                break
            print(f"Deleting {len(items)} old records...")
            for item in items:
                requests.delete(f"{PB_URL}/api/collections/global_top/records/{item['id']}", headers=headers)
        else:
            break
    
    # Insert new records
    print("Inserting new global rankings...")
    for r in sorted_rankings:
        record_data = {
            "name": r.get('name', ''),
            "address": r.get('address', ''),
            "city": r.get('city', 'Unknown'),
            "google_place_id": r.get('google_place_id', ''),
            "place_id": r.get('id', ''),
            "lat": r.get('latitude', 0),
            "lng": r.get('longitude', 0),
            "photo_url": r.get('photo_url', ''),
            "rating": r.get('rating', 0),
            "total_reviews": r.get('total_reviews', 0),
            "rank_score": r.get('rank_score', 0),
            "ai_score": r.get('ai_score', 0),
            "has_ai_analysis": r.get('has_ai_analysis', False),
            "global_rank": r.get('global_rank', 0),
            "rank_change": r.get('rank_change', 0),
            "rank_change_indicator": r.get('rank_change_indicator', 'neutral'),
            "is_new": r.get('is_new', False),
            "opening_hours": r.get('opening_hours')
        }
        resp = requests.post(
            f"{PB_URL}/api/collections/global_top/records",
            json=record_data,
            headers=headers
        )
        if resp.status_code in [200, 201]:
            trend_str = ""
            if r.get('is_new'): trend_str = "[NEW]"
            elif r.get('rank_change_indicator') == 'up': trend_str = f"[▲{r['rank_change']}]"
            elif r.get('rank_change_indicator') == 'down': trend_str = f"[▼{abs(r['rank_change'])}]"
            
            print(f"  #{r['global_rank']:>2}. {r['name'][:30]:<30} {trend_str:<6} Score: {r['rank_score']:.1f} - City: {r['city']}")
        else:
            print(f"  ❌ Failed to insert {r['name']}: {resp.text[:100]}")
    
    print(f"\n✅ Global top populated with {len(sorted_rankings)} rankings!")


if __name__ == "__main__":
    print("=== Creating/Updating global_top collection ===")
    if create_global_top_collection():
        print("\n=== Populating global_top ===")
        populate_global_top()
