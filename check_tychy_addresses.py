import os
import sys
import io
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_tychy_addresses():
    load_dotenv()
    pb_url = os.getenv('PB_URL')
    pb = PocketbaseService(pb_url)
    pb._ensure_auth()
    
    city_id = pb.get_city_id("Tychy")
    if not city_id:
        print("Tychy not found.")
        return

    # Fetch rank records for latest batch
    # (Since I don't have a direct "get all places for city" that's easy, 
    # I'll use the get_city_rankings logic or just list collection)
    
    records = pb.client.collection('kebab_places').get_full_list(query_params={
        "filter": f'city="{city_id}"'
    })
    
    print(f"Total places in Tychy collection: {len(records)}")
    
    # Sort for easier reading if needed, but let's just print them
    for i, r in enumerate(records):
        print(f"{i+1}. {r.name} | Address: {r.address}")

if __name__ == "__main__":
    check_tychy_addresses()
