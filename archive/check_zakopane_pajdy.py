
import os
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

def check_zakopane():
    load_dotenv()
    pb = PocketbaseService(os.getenv("PB_URL"), os.getenv("PB_EMAIL"), os.getenv("PB_PASSWORD"))
    pb._ensure_auth()
    
    # Search for Kebab u Pajdy in Zakopane
    results = pb.client.collection('kebab_places').get_list(1, 10, {
        "filter": 'name ~ "Pajdy" && address ~ "Jagiell"'
    })
    
    for item in results.items:
        print(f"ID: {item.id}")
        print(f"Name: {item.name}")
        print(f"Address: {item.address}")
        print(f"Photo: '{getattr(item, 'photo', 'N/A')}'")
        print("-" * 20)

if __name__ == "__main__":
    check_zakopane()
