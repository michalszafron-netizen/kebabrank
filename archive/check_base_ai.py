import os
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

load_dotenv()

db = PocketbaseService(os.getenv('PB_URL'), os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))
db._ensure_auth()

def check_ratings_fields():
    city_id = db.get_city_id("Kraków")
    res = db.client.collection('ratings').get_list(
        1, 10,
        query_params={
            "filter": f'kebab_place.city="{city_id}"',
            "sort": "-created",
            "expand": "kebab_place"
        }
    )
    
    print(f"Checking top 10 ratings for Kraków...")
    for i, r in enumerate(res.items):
        place = getattr(r, "expand", {}).get("kebab_place")
        name = place.name if place else "Unknown"
        # Explicitly check for ai_score in the rating record
        ai_score = getattr(r, 'ai_score', 'N/A')
        rank_score = getattr(r, 'rank_score', 'N/A')
        print(f"#{i+1}: {name} | Rating ai_score: {ai_score} | rank_score: {rank_score}")

if __name__ == "__main__":
    check_ratings_fields()
