import os
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService
from datetime import datetime, timedelta

load_dotenv()
pb = PocketbaseService(os.getenv('PB_URL'))
city_id = pb.get_city_id('Kraków')

records = pb.client.collection('ratings').get_list(
    1, 5000, 
    query_params={
        "filter": f'kebab_place.city="{city_id}"',
        "sort": "-created",
        "expand": "kebab_place"
    }
)

print(f"Total records fetched for Kraków: {len(records.items)}")
if records.items:
    print(f"Latest record time: {records.items[0].created}")
    print(f"Oldest record time: {records.items[-1].created}")
