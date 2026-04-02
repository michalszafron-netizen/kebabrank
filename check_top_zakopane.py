import os
import sys
import io
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_top_zakopane():
    load_dotenv()
    pb_url = os.getenv('PB_URL')
    pb = PocketbaseService(pb_url)
    
    rankings = pb.get_city_rankings('Zakopane')
    print(f"Total places in Zakopane: {len(rankings)}")
    print("\nTop 5 Places:")
    for i, kebab in enumerate(rankings[:5]):
        print(f"{i+1}. {kebab['name']} (ID: {kebab['id']}, Score: {kebab['rank_score']})")

if __name__ == "__main__":
    check_top_zakopane()
