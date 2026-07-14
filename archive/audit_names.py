import os
import sys
import io
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def audit_ids_names():
    load_dotenv()
    pb = PocketbaseService(os.getenv('PB_URL'))
    
    city_id = pb.get_city_id("Zakopane")
    print(f"Zakopane ID: {city_id}")
    
    # Get all places
    places = pb.client.collection('kebab_places').get_full_list(query_params={'filter': f'city="{city_id}"'})
    print(f"\nTotal places in DB: {len(places)}")
    
    # Sort by created
    places.sort(key=lambda x: x.created, reverse=True)
    
    print("\nRecent places:")
    for p in places[:10]:
        print(f"[{p.created}] ID: {p.google_place_id} | Name: {p.name}")
        
    print("\nOlder places:")
    for p in places[-10:]:
        print(f"[{p.created}] ID: {p.google_place_id} | Name: {p.name}")

if __name__ == "__main__":
    audit_ids_names()
