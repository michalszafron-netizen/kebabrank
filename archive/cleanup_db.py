import os
from dotenv import load_dotenv
load_dotenv()
from services.pocketbase_db import PocketbaseService
pb = PocketbaseService(os.environ.get("PB_URL"))
pb._ensure_auth()
try:
    city_name = "Chorzów"
    city_id = pb.get_city_id(city_name)
    print(f"City ID: {city_id}")
    
    places = pb.client.collection("kebab_places").get_full_list(
        query_params={"filter": f"city='{city_id}'"}
    )
    
    count_reset = 0
    count_kept = 0
    for p in places:
        full_address = getattr(p, 'address', '').lower()
        if city_name.lower() not in full_address:
            # Does not contain Chorzow -> set to 0 to make it a ghost
            pb.client.collection("kebab_places").update(p.id, {"city_rank": 0})
            print(f"Skipped and reset to 0: {getattr(p, 'name')} ({full_address})")
            count_reset += 1
        else:
            count_kept += 1
            print(f"Kept: {getattr(p, 'name')}")
            
    print(f"Reset {count_reset} places. Kept {count_kept} places.")
    print("Recalculating absolute rankings in DB for remaining...")
    pb.recalculate_city_rankings(city_id)
    print("DONE! Fixed the database zero API tokens consumed.")
    
except Exception as e:
    print(e)
