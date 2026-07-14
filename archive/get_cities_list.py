
import os
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

def main():
    load_dotenv()
    pb = PocketbaseService(os.getenv('PB_URL'))
    cities = sorted([c['name'] for c in pb.get_cities()])
    with open('_cities.tmp', 'w', encoding='utf-8') as f:
        f.write('\n'.join(cities))
    print(f"Saved {len(cities)} cities to _cities.tmp")

if __name__ == "__main__":
    main()
