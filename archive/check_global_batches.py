import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from dotenv import load_dotenv
from pocketbase import PocketBase
load_dotenv()

pb = PocketBase(os.getenv('PB_URL'))
pb.collection("_superusers").auth_with_password(os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))

# Fetch last 5000 ratings
recs = pb.collection('ratings').get_list(
    1, 5000,
    query_params={
        "sort": "-created"
    }
)

print(f"Global Ranking batches (last 5000):")
batches = {}
for r in recs.items:
    if hasattr(r.created, 'strftime'):
        t = r.created.strftime("%Y-%m-%d %H")
    else:
        t = str(r.created)[:13]
    batches[t] = batches.get(t, 0) + 1

for b in sorted(batches.keys(), reverse=True):
    print(f"  {b}: {batches[b]} records")
