import os
import sys
import io
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def list_all_cities():
    load_dotenv()
    pb_url = os.getenv('PB_URL')
    pb = PocketbaseService(pb_url)
    pb._ensure_auth()
    
    cities = pb.client.collection('cities').get_full_list()
    city_names = [c.name for c in cities]
    print(f"TOTAL_CITIES: {len(city_names)}")
    print(f"CITIES_LIST: {', '.join(city_names)}")

if __name__ == "__main__":
    list_all_cities()
