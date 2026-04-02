
import os
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

def check_place():
    load_dotenv()
    pb_url = os.getenv("PB_URL")
    pb_email = os.getenv("PB_EMAIL")
    pb_password = os.getenv("PB_PASSWORD")
    
    pb = PocketbaseService(pb_url, pb_email, pb_password)
    pb._ensure_auth()
    
    # Search for Siesta Burger Zakopane
    try:
        results = pb.client.collection('kebab_places').get_list(1, 10, {
            "filter": 'name ~ "Siesta Burger"'
        })
        
        for item in results.items:
            print(f"ID: {item.id}")
            print(f"Name: {item.name}")
            print(f"Photo: '{getattr(item, 'photo', 'N/A')}'")
            print(f"Image URL (legacy): '{getattr(item, 'image_url', 'N/A')}'")
            print("-" * 20)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_place()
