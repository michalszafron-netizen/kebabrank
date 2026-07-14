"""
One-off script: removes a closed/permanently-closed place from kebab_places.
Usage: python remove_closed_place.py "Meat & Sandwich" Zakopane
"""
import os, sys, io
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()

def remove_place(name: str, city: str):
    pb = PocketbaseService(os.getenv('PB_URL'), os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))

    city_id = pb.get_city_id(city)
    if not city_id:
        print(f"City '{city}' not found.")
        return

    try:
        records = pb.client.collection('kebab_places').get_full_list(
            query_params={"filter": f'city="{city_id}" && name~"{name}"'}
        )
    except Exception as e:
        print(f"Error fetching: {e}")
        return

    if not records:
        print(f"No place found matching '{name}' in {city}.")
        return

    for rec in records:
        print(f"Found: {rec.name} (id={rec.id}) — confirm deletion? [y/N]: ", end='')
        answer = input().strip().lower()
        if answer == 'y':
            pb.client.collection('kebab_places').delete(rec.id)
            print(f"  Deleted {rec.name}.")
        else:
            print(f"  Skipped.")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python remove_closed_place.py <name> <city>")
        sys.exit(1)
    remove_place(sys.argv[1], sys.argv[2])
