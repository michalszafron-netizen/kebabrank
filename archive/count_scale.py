import os
from dotenv import load_dotenv
from pocketbase import PocketBase

load_dotenv()
pb = PocketBase(os.getenv('PB_URL'))
pb.admins.auth_with_password(os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))

cities = pb.collection('cities').get_full_list()
print(f"Total Cities: {len(cities)}")

# Check top 5 for each city
# Actually just count total places for an 'update'
# Assume an update scrapes all cities
# How many places per city?
# Let's count current ratings to see the scale of the last update
ratings = pb.collection('ratings').get_list(1, 1, query_params={"sort": "-created"})
if ratings.items:
    latest_time = ratings.items[0].created
    # Count all ratings in the last 60 mins of that timestamp
    # (Scale of one update batch)
    from datetime import datetime, timedelta
    if isinstance(latest_time, str):
        # Replace 'Z' and handles fractional seconds
        clean_time = latest_time.replace('Z', '+00:00')
        latest_dt = datetime.fromisoformat(clean_time)
    else:
        latest_dt = latest_time
    
    # Format for PB query
    window_start = (latest_dt - timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")
    batch = pb.collection('ratings').get_full_list(query_params={"filter": f'created >= "{window_start}"'})
    print(f"Places in most recent batch: {len(batch)}")
else:
    print("No ratings found.")
