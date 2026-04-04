import os
import sys
import io
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from services.pocketbase_db import PocketbaseService
from services.serper_service import SerperService
from services.ai_data_updater import AIDataUpdater

def update_city_review_ai(city_name: str, limit: int = 5):
    load_dotenv()
    
    pb_url = os.getenv('PB_URL')
    serper_key = os.getenv('SERPER_API_KEY')
    deepseek_key = os.getenv('DEEPSEEK_API_KEY')
    
    if not serper_key:
        print("Error: SERPER_API_KEY not found in .env.")
        return
    if not deepseek_key:
        print("Error: DEEPSEEK_API_KEY not found.")
        return

    pb = PocketbaseService(pb_url)
    serper = SerperService(serper_key)
    
    ai_updater = AIDataUpdater(pb, serper, deepseek_key)
    
    print(f"--- Running AI Analysis for {city_name} (Top {limit}) ---")
    try:
        ai_updater.update_ai_analysis_for_city(city_name, limit=limit)
        print(f"\nAI analysis complete for {city_name}")
    except Exception as e:
        print(f"Error during AI analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('cities', nargs='+', help='One or more city names')
    parser.add_argument('--limit', type=int, default=5, help='Number of top places to analyze')
    args = parser.parse_args()
    
    for city in args.cities:
        update_city_review_ai(city, args.limit)

