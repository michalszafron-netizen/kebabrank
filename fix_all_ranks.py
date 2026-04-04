import os
import sys
from dotenv import load_dotenv
load_dotenv()

from services.pocketbase_db import PocketbaseService

pb = PocketbaseService(os.environ.get("PB_URL"))
pb._ensure_auth()

print("[FIX] Restoring city_rank for ALL places from ratings history...")

# Get all cities
cities = pb.client.collection("cities").get_full_list()
print(f"Found {len(cities)} cities to restore.")

total_fixed = 0

for city in cities:
    city_id = city.id
    city_name = getattr(city, "name", city_id)
    
    try:
        # Get latest ratings for this city, sorted by rank_score desc
        ratings = pb.client.collection("ratings").get_full_list(
            query_params={
                "filter": f'kebab_place.city="{city_id}"',
                "sort": "-rank_score,-total_reviews",
                "expand": "kebab_place"
            }
        )
        
        if not ratings:
            print(f"  {city_name}: no ratings found, skipping")
            continue
        
        # Deduplicate - one rating per place (latest/highest score)
        seen_places = {}
        for r in ratings:
            p = getattr(r, "expand", {}).get("kebab_place")
            if not p:
                continue
            if p.id not in seen_places:
                seen_places[p.id] = r
        
        # Sort by rank_score
        sorted_ratings = sorted(seen_places.values(), key=lambda x: (getattr(x, "rank_score", 0), getattr(x, "total_reviews", 0)), reverse=True)
        
        # Restore city_rank in kebab_places
        for i, r in enumerate(sorted_ratings):
            p = getattr(r, "expand", {}).get("kebab_place")
            if not p:
                continue
            new_rank = i + 1
            try:
                pb.client.collection("kebab_places").update(p.id, {"city_rank": new_rank})
                total_fixed += 1
            except Exception as e:
                print(f"  Error updating {getattr(p, 'name', p.id)}: {e}")
        
        print(f"  {city_name}: restored {len(sorted_ratings)} places")
    except Exception as e:
        print(f"  {city_name}: ERROR - {e}")

print(f"\n[DONE] Restored city_rank for {total_fixed} places total.")
print("Now restart Flask to clear cache.")
