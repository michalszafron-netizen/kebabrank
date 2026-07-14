# check_rank_changes.py - Verify if ranks actually changed between dates
import os
from datetime import datetime
from dotenv import load_dotenv
from services.database import DatabaseService

load_dotenv()

def check_rank_changes():
    """Check if kebab ranks actually changed between the two dates"""
    db_service = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    
    print("🔍 Checking if ranks actually changed between dates...")
    print("=" * 60)
    
    test_city = "Kraków"
    city_id = db_service.get_city_id(test_city)
    
    if not city_id:
        print(f"❌ City {test_city} not found")
        return
    
    # Get all kebabs in the city
    kebabs = db_service.client.table('kebab_places').select(
        'id, name, google_place_id'
    ).eq('city_id', city_id).execute()
    
    if not kebabs.data:
        print("❌ No kebabs found")
        return
    
    print(f"📊 Analyzing rank changes for {len(kebabs.data)} kebabs in {test_city}\n")
    
    changes_found = False
    
    for kebab in kebabs.data[:10]:  # Check first 10 kebabs
        # Get all historical rankings for this kebab
        history = db_service.client.table('ratings_history').select(
            'city_rank, data_fetched_at, rating, total_reviews'
        ).eq('kebab_place_id', kebab['id']).order(
            'data_fetched_at', desc=True
        ).execute()
        
        if len(history.data) >= 2:
            latest = history.data[0]
            previous = history.data[-1]  # Oldest entry
            
            rank_change = previous['city_rank'] - latest['city_rank']
            
            print(f"🥙 {kebab['name'][:40]}...")
            print(f"   📅 July 9:  Rank #{previous['city_rank']} (Rating: {previous['rating']}, Reviews: {previous['total_reviews']})")
            print(f"   📅 July 24: Rank #{latest['city_rank']} (Rating: {latest['rating']}, Reviews: {latest['total_reviews']})")
            
            if rank_change != 0:
                changes_found = True
                if rank_change > 0:
                    print(f"   ✅ MOVED UP {rank_change} places! ↑")
                else:
                    print(f"   ❌ MOVED DOWN {abs(rank_change)} places! ↓")
            else:
                print(f"   ➡️  No change in rank")
            
            print()
    
    if not changes_found:
        print("\n⚠️  NO RANK CHANGES FOUND!")
        print("This explains why all kebabs show 'No change'")
        print("\nPossible reasons:")
        print("1. Rankings were recalculated but resulted in the same order")
        print("2. No new reviews were added between July 9 and July 24")
        print("3. The ranking algorithm produces very stable results")
    else:
        print("\n✅ Rank changes detected! The system should be working correctly.")
    
    # Show date distribution
    print("\n" + "=" * 60)
    print("📅 Date distribution of your data:")
    
    date_dist = db_service.client.table('ratings_history').select(
        'data_fetched_at'
    ).execute()
    
    if date_dist.data:
        dates = {}
        for record in date_dist.data:
            date_str = record['data_fetched_at'].split('T')[0]
            dates[date_str] = dates.get(date_str, 0) + 1
        
        for date, count in sorted(dates.items()):
            print(f"   {date}: {count} records")

if __name__ == "__main__":
    check_rank_changes()