import os
from dotenv import load_dotenv
from pocketbase import PocketBase

load_dotenv()

PB_URL = os.getenv("PB_URL")
PB_EMAIL = os.getenv("PB_EMAIL")
PB_PASSWORD = os.getenv("PB_PASSWORD")

import sys
import io

# Set stdout to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def debug_kebab_place():
    pb = PocketBase(PB_URL)
    pb.collection("_superusers").auth_with_password(PB_EMAIL, PB_PASSWORD)
    
    print(f"Connected to {PB_URL}")
    
    # Fetch a few kebab places
    places = pb.collection('kebab_places').get_list(1, 10)
    
    if not places.items:
        print("No kebab places found.")
        return
        
    for p in places.items:
        print(f"\n--- Kebab Place: {p.name} ---")
        print(f"ID: {p.id}")
        print(f"Available fields: {vars(p).keys()}")
        
        # Print actual values for relevant fields
        for field in ['city', 'address', 'google_place_id']:
            val = getattr(p, field, 'MISSING')
            print(f"  {field}: {val}")
        
        city_id = getattr(p, 'city', None)
        if city_id:
            try:
                city = pb.collection('cities').get_one(city_id)
                print(f"  City Name from ID: {getattr(city, 'name', 'N/A')}")
            except Exception as e:
                print(f"  Error fetching city {city_id}: {e}")
        else:
            print("  No City ID found on place.")

if __name__ == "__main__":
    debug_kebab_place()
