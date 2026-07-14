
import os
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

def check_all_photos():
    load_dotenv()
    pb_url = os.getenv("PB_URL")
    pb_email = os.getenv("PB_EMAIL")
    pb_password = os.getenv("PB_PASSWORD")
    
    pb = PocketbaseService(pb_url, pb_email, pb_password)
    pb._ensure_auth()
    
    try:
        # Check how many have photos
        results = pb.client.collection('kebab_places').get_list(1, 100, {
            "filter": 'photo != ""'
        })
        
        print(f"Total places with photos: {results.total_items}")
        for item in results.items[:5]:
            print(f" - {item.name}: {item.photo}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_all_photos()
