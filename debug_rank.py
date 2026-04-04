
import os
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

def main():
    load_dotenv()
    pb = PocketbaseService(os.getenv('PB_URL'))
    
    city_id = pb.get_city_id('Chorzów')
    print(f"Chorzów ID: {city_id}")
    
    try:
        place = pb.client.collection('kebab_places').get_first_list_item('name="Wolf Kebab"')
        print(f"Wolf Kebab city_rank: {getattr(place, 'city_rank', 'Missing')}")
    except Exception as e:
        print(f"Wolf Kebab not found: {e}")

if __name__ == "__main__":
    main()
