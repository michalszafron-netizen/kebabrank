import os
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

load_dotenv()

db = PocketbaseService(os.getenv('PB_URL'), os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))
db._ensure_auth()

def check_counts():
    print(f"Total AI Analysis items: {db.client.collection('ai_analysis').get_list(1,1).total_items}")
    
    cities = db.get_cities()
    for c in cities:
        if c['name'] in ["Warszawa", "Kraków", "Wrocław"]:
            c_id = c['id']
            ai_count = db.client.collection('ai_analysis').get_list(1, 1, query_params={'filter': f'kebab_place.city="{c_id}"'}).total_items
            r_count = db.client.collection('ratings').get_list(1, 1, query_params={'filter': f'kebab_place.city="{c_id}"'}).total_items
            print(f"City: {c['name']} (ID: {c_id}) | AI: {ai_count} | Ratings: {r_count}")

    # Verify latest ranking for Kraków again
    k_rankings = db.get_city_rankings("Kraków", limit=15)
    print(f"\nKraków Top 15 count: {len(k_rankings)}")
    for i, r in enumerate(k_rankings):
        print(f"  #{i+1} {r['name']} - Score: {r['rank_score']} (AI: {r.get('has_ai_analysis')})")

if __name__ == "__main__":
    check_counts()
