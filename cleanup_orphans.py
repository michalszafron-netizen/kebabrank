import os, sys, io
from dotenv import load_dotenv
from pocketbase import PocketBase

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()
pb = PocketBase(os.getenv('PB_URL'))
pb.admins.auth_with_password(os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))

print("Searching for orphan records (city == '')...")
# Get all places with empty city
orphans = pb.collection('kebab_places').get_full_list(query_params={"filter": "city = ''"})
total = len(orphans)
print(f"Found {total} orphan records to delete.")

count = 0
for p in orphans:
    try:
        pb.collection('kebab_places').delete(p.id)
        count += 1
        if count % 100 == 0:
            print(f"Deleted {count}/{total}...")
    except Exception as e:
        print(f"Error deleting {p.id}: {e}")

print(f"\nCleanup complete. Total deleted: {count}")
