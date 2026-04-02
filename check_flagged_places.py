
import os
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

def check_specific():
    load_dotenv()
    pb = PocketbaseService(os.getenv("PB_URL"), os.getenv("PB_EMAIL"), os.getenv("PB_PASSWORD"))
    pb._ensure_auth()
    
    names = ["Kebab u Pajdy", "Wołowiec i Kura"]
    for name in names:
        results = pb.client.collection('kebab_places').get_list(1, 5, {
            "filter": f'name ~ "{name}"'
        })
        for item in results.items:
            print(f"Name: {item.name}")
            print(f"Photo field: '{getattr(item, 'photo', 'N/A')}'")
            print("-" * 20)

if __name__ == "__main__":
    check_specific()
