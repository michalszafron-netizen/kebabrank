import os
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

load_dotenv()

db = PocketbaseService(os.getenv('PB_URL'), os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))
db._ensure_auth()

def check_krakow_ai():
    city_id = db.get_city_id("Kraków")
    print(f"Kraków City ID: {city_id}")
    
    # Check AI analysis directly
    ai_res = db.client.collection('ai_analysis').get_list(
        1, 10,
        query_params={
            "filter": f'kebab_place.city="{city_id}"'
        }
    )
    print(f"AI Analysis items for Kraków city: {ai_res.total_items}")
    
    # Check ratings batch spread
    ratings_res = db.client.collection('ratings').get_list(
        1, 50,
        query_params={
            "filter": f'kebab_place.city="{city_id}"',
            "sort": "-created"
        }
    )
    timestamps = [r.created for r in ratings_res.items]
    from collections import Counter
    print(f"Rating timestamps distribution (latest 50): {Counter(timestamps)}")

    # Check Warszawa batch spread
    w_id = db.get_city_id("Warszawa")
    w_ratings = db.client.collection('ratings').get_list(
        1, 50,
        query_params={
            "filter": f'kebab_place.city="{w_id}"',
            "sort": "-created"
        }
    )
    w_timestamps = [r.created for r in w_ratings.items]
    print(f"Warszawa timestamps distribution (latest 50): {Counter(w_timestamps)}")

if __name__ == "__main__":
    check_krakow_ai()
