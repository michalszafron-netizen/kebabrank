import os, sys, io
from dotenv import load_dotenv
from pocketbase import PocketBase

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()
pb = PocketBase(os.getenv('PB_URL'))
pb.admins.auth_with_password(os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))

# Get all linked places
linked_places = pb.collection('kebab_places').get_full_list(query_params={"filter": "city != ''"})
linked_names = {p.name.lower().strip() for p in linked_places}

# Get a sample of unknown places
unknown_places = pb.collection('kebab_places').get_list(1, 100, query_params={"filter": "city = ''"})

print(f"Linked Places: {len(linked_places)}")
print(f"Unknown Places: {unknown_places.total_items}")

duplicates_found = 0
for p in unknown_places.items:
    if p.name.lower().strip() in linked_names:
        duplicates_found += 1

print(f"\nIn first 100 unknown places, {duplicates_found} have the same name as a linked place.")

print("\nSample Unknown Places Details:")
for p in unknown_places.items[:10]:
    is_dub = "DUPLICATE NAME" if p.name.lower().strip() in linked_names else "UNIQUE NAME"
    print(f"  [{is_dub}] {p.name} | {p.address}")
