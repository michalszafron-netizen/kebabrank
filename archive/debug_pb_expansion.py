import os
from dotenv import load_dotenv
from pocketbase import PocketBase

load_dotenv()

PB_URL = os.getenv("PB_URL")
PB_EMAIL = os.getenv("PB_EMAIL")
PB_PASSWORD = os.getenv("PB_PASSWORD")

def debug_global_expansion():
    pb = PocketBase(PB_URL)
    pb.collection("_superusers").auth_with_password(PB_EMAIL, PB_PASSWORD)
    
    print(f"Connected to {PB_URL}")
    
    records = pb.collection('ratings').get_list(
        1, 1,
        query_params={
            "sort": "-rank_score",
            "expand": "kebab_place,kebab_place.city"
        }
    )
    
    if not records.items:
        print("No records found.")
        return
        
    r = records.items[0]
    print("\n--- Rating Record ---")
    print(f"ID: {r.id}")
    
    # PocketBase SDK expands
    # Let's try to see if it's in a hidden field or some other alias
    print(f"\n--- RAW Record Data ---")
    # Some PB SDKs have a ._data or a .data attribute
    raw_data = getattr(r, "_data", {})
    if not raw_data:
        raw_data = getattr(r, "data", {})
    
    if raw_data:
        print(f"Raw Data Keys: {raw_data.keys()}")
        if "expand" in raw_data:
            print(f"Raw Expand Keys: {raw_data['expand'].keys()}")
    
    # Try another way: maybe it's nested differently
    print(f"\nVars(r): {vars(r).keys()}")
    
    expand1 = getattr(r, "expand", {})
    if not expand1:
        # Fallback to _expand
        expand1 = getattr(r, "_expand", {})
        
    print(f"Final Expand Keys (level 1): {expand1.keys() if expand1 else 'None'}")

if __name__ == "__main__":
    debug_global_expansion()
