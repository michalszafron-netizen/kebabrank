import os
import sys
import io
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def inspect_kebab_fields():
    load_dotenv()
    pb_url = os.getenv('PB_URL')
    pb = PocketbaseService(pb_url)
    pb._ensure_auth()
    
    # Get one record from kebab_places
    records = pb.client.collection('kebab_places').get_list(1, 1)
    if records.items:
        item = records.items[0]
        print("Fields in kebab_places record:")
        for key, value in item.__dict__.items():
            if key not in ['collection_id', 'collection_name']:
                print(f"  {key}: {type(value)}")
                if key in ['name', 'image', 'photo', 'logo', 'icon']:
                    print(f"    Value: {value}")

if __name__ == "__main__":
    inspect_kebab_fields()
