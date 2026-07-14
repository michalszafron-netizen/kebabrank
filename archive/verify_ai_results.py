import os
import sys
import io
import json
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verify_ai_results():
    load_dotenv()
    pb_url = os.getenv('PB_URL')
    pb = PocketbaseService(pb_url)
    pb._ensure_auth()
    
    # Get top 5 in Zakopane
    rankings = pb.get_city_rankings('Zakopane')
    
    print(f"Top 5 AI Analysis Results for Zakopane:\n")
    for kebab in rankings[:5]:
        print(f"--- {kebab['name']} ---")
        print(f"Original Rank Score: {kebab.get('rank_score', 0)}")
        print(f"AI Score: {kebab.get('ai_score', 'N/A')}")
        
        # Query ai_analysis collection directly
        try:
            place_id = pb.get_place_id(kebab['google_place_id'])
            ai_record = pb.client.collection('ai_analysis').get_first_list_item(f'kebab_place="{place_id}"')
            if ai_record:
                print(f"AI Summary: {ai_record.ai_summary}")
                print(f"AI Confidence: {ai_record.confidence_score}")
                # Print a bit of the raw data to see details
                data = ai_record.analysis_data
                sentiment = data.get('sentiment_analysis', {})
                authenticity = data.get('authenticity_analysis', {})
                print(f"AI Sentiment Score: {sentiment.get('average_sentiment', 'N/A')}")
                print(f"AI Authenticity Score: {authenticity.get('authenticity_score', 'N/A')}%")
            else:
                print("No AI record found in ai_analysis collection.")
        except Exception as e:
            print(f"Error fetching AI analysis record: {e}")
        
        print("-" * 20)

if __name__ == "__main__":
    verify_ai_results()
