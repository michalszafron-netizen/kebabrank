import os
import sys
import io
import argparse
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def _get_sentiment_label(score: float) -> str:
    """Same logic as AIDataUpdater"""
    if score > 0.6: return 'absolutny zachwyt'
    elif score > 0.3: return 'bardzo pozytywne'
    elif score > 0.1: return 'lekki entuzjazm'
    elif score < -0.6: return 'miażdżąca krytyka'
    elif score < -0.3: return 'wyraźna niechęć'
    elif score < -0.1: return 'lekkie rozczarowanie'
    else: return 'mieszane odczucia'

def verify_ai_results(city_name):
    load_dotenv()
    pb_url = os.getenv('PB_URL')
    pb = PocketbaseService(pb_url)
    pb._ensure_auth()
    
    print(f"--- AI Analysis Results for {city_name} ---\n")
    
    # Get top 5 in city
    rankings = pb.get_city_rankings(city_name)
    
    for kebab in rankings[:5]:
        print(f"--- {kebab['name']} ---")
        print(f"Points: {kebab.get('rank_score', 0):.2f} -> AI Score: {kebab.get('ai_score', 'N/A')}")
        
        # Query ai_analysis collection
        try:
            place_id = pb.get_place_id(kebab['google_place_id'])
            ai_record = pb.client.collection('ai_analysis').get_first_list_item(f'kebab_place="{place_id}"')
            if ai_record:
                print(f"AI Summary: {ai_record.ai_summary}")
                data = ai_record.analysis_data
                sentiment = data.get('sentiment_analysis', {})
                trend = data.get('trend_analysis', {})
                sentiment_val = sentiment.get('average_sentiment', 0)
                print(f"Sentiment: {sentiment_val} ({_get_sentiment_label(sentiment_val)})")
                print(f"Trend: {trend.get('trend', 'N/A')}")
                print(f"Expert Tip: {data.get('creative_insight', 'N/A')}")
            else:
                print("No AI record found.")
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 20)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('city', help='City name')
    args = parser.parse_args()
    verify_ai_results(args.city)
