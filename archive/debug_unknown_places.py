import os
from dotenv import load_dotenv
from pocketbase import PocketBase

load_dotenv()
pb = PocketBase(os.getenv('PB_URL'))
pb.admins.auth_with_password(os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))

# Find places with no city linked (city field is empty or points to a non-existent ID)
# First get all city IDs to check validity
cities = pb.collection('cities').get_full_list()
valid_city_ids = {c.id for c in cities}

# Sample 20 'Unknown' places
unknown_places = pb.collection('kebab_places').get_list(1, 100, query_params={"filter": "city = ''"})
# Also check if it points to an invalid ID
all_places = pb.collection('kebab_places').get_full_list()
invalid_links = [p for p in all_places if p.city and p.city not in valid_city_ids]

print(f"Places with empty city: {unknown_places.total_items}")
print(f"Places with invalid city ID: {len(invalid_links)}")

print("\nSample Unknown Places (Empty City):")
for p in unknown_places.items[:10]:
    print(f"  Name: {p.name} | Address: {p.address} | Created: {p.created}")

if invalid_links:
    print("\nSample Invalid City Link Places:")
    for p in invalid_links[:10]:
        print(f"  Name: {p.name} | City ID: {p.city} | Created: {p.created}")
