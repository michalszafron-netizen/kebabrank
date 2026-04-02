import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from dotenv import load_dotenv
from pocketbase import PocketBase
load_dotenv()

pb = PocketBase(os.getenv('PB_URL'))
pb.collection("_superusers").auth_with_password(os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))

# Total count
total = pb.collection('ratings').get_list(1, 1).total_items
print(f"Total ratings in DB: {total}")

# Get the oldest 100 records
oldest = pb.collection('ratings').get_list(1, 100, query_params={"sort": "created"})
print(f"\nOldest timestamps:")
for r in oldest.items:
    print(f"  {r.created}")
    break # Just show first
print(f"  ... (last in oldest 100) {oldest.items[-1].created}")

# Get unique years/months
# Pocketbase doesn't support grouping well, so let's just sample
print(f"\nSampling different parts of the collection:")
for page in [1, 100, 500, 1000]:
    try:
        sample = pb.collection('ratings').get_list(page, 1, query_params={"sort": "created"})
        if sample.items:
            print(f"  Page {page}: {sample.items[0].created}")
    except: pass
