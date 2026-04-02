import os
import io
import sys
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def dump_zakopane_places():
    load_dotenv()
    pb = PocketbaseService(os.getenv('PB_URL'))
    
    city_name = "Zakopane"
    city_id = pb.get_city_id(city_name)
    
    places = pb.client.collection('kebab_places').get_full_list(query_params={'filter': f'city="{city_id}"', 'sort': 'created'})
    
    print(f"--- Kebab Places in Zakopane ({len(places)}) ---")
    for p in places:
        print(f"Created: {p.created} | Name: {p.name} | G_ID: {p.google_place_id} | ID: {p.id}")

if __name__ == "__main__":
    dump_zakopane_places()
