import os
from dotenv import load_dotenv
from pocketbase import PocketBase
from datetime import datetime, timezone

load_dotenv()

PB_URL = os.getenv("PB_URL")
PB_EMAIL = os.getenv("PB_EMAIL")
PB_PASSWORD = os.getenv("PB_PASSWORD")

import sys
import io

# Set stdout to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_ranking_freshness():
    pb = PocketBase(PB_URL)
    pb.collection("_superusers").auth_with_password(PB_EMAIL, PB_PASSWORD)
    
    print(f"Connected to {PB_URL}")
    
    # 1. Search for records created today (Feb 27)
    print("\n--- Ratings created on 2026-02-27 ---")
    today_records = pb.collection('ratings').get_list(
        1, 10, 
        query_params={
            "filter": 'created >= "2026-02-27 00:00:00"',
            "sort": "-created",
            "expand": "kebab_place"
        }
    )
    if not today_records.items:
        print("No records found for today (Feb 27).")
    for r in today_records.items:
        place = getattr(r, "expand", {}).get("kebab_place")
        name = getattr(place, "name", "N/A") if place else "N/A"
        print(f"Score: {r.rank_score} | Created: {r.created} | Name: {name}")

    # 2. Specifically look at Kebab DRWAL (Gdańsk)

if __name__ == "__main__":
    check_ranking_freshness()
