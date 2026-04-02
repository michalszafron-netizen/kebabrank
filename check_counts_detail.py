import os
from dotenv import load_dotenv
from pocketbase import PocketBase

load_dotenv()
pb = PocketBase(os.getenv('PB_URL'))
pb.admins.auth_with_password(os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))

# Total unique kebab places
places = pb.collection('kebab_places').get_list(1, 1)
total_places = places.total_items
print(f"Total Unique Kebab Places: {total_places}")

# Total ratings/rankings records
ratings = pb.collection('ratings').get_list(1, 1)
total_ratings = ratings.total_items
print(f"Total Ratings Records (History): {total_ratings}")

# Check distribution of created timestamps in ratings
recent_ratings = pb.collection('ratings').get_list(1, 100, query_params={"sort": "-created"})
if recent_ratings.items:
    print("\nRecent Review Timestamps:")
    for r in recent_ratings.items[:10]:
        print(f"  {r.created}")

# Count unique google_place_id in ratings if possible
# Or just look at the most recent hour again more carefully
from datetime import datetime, timedelta
latest_time = recent_ratings.items[0].created
if isinstance(latest_time, str):
    latest_dt = datetime.fromisoformat(latest_time.replace('Z', '+00:00'))
else:
    latest_dt = latest_time

window_start = (latest_dt - timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")
# Full list is expensive, let's just use total_items with filter
batch_meta = pb.collection('ratings').get_list(1, 1, query_params={"filter": f'created >= "{window_start}"'})
print(f"\nRatings created in the last 60 mins of latest record: {batch_meta.total_items}")
