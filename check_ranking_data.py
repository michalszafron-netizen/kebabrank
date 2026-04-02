# check_ranking_data.py - Improved script with better timestamp handling
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from services.database import DatabaseService

load_dotenv()

def parse_timestamp(timestamp_str):
    """Parse timestamp string handling various formats"""
    if not timestamp_str:
        return None
    
    # Remove 'Z' suffix if present
    if timestamp_str.endswith('Z'):
        timestamp_str = timestamp_str[:-1] + '+00:00'
    
    # Try different parsing methods
    try:
        # First try standard isoformat
        return datetime.fromisoformat(timestamp_str)
    except ValueError:
        try:
            # Handle microseconds with more than 6 digits
            if '.' in timestamp_str and '+' not in timestamp_str and 'T' in timestamp_str:
                # Split into parts
                date_part, time_part = timestamp_str.split('T')
                if '.' in time_part:
                    time_main, microseconds = time_part.split('.')
                    # Truncate microseconds to 6 digits
                    microseconds = microseconds[:6]
                    timestamp_str = f"{date_part}T{time_main}.{microseconds}"
                    return datetime.fromisoformat(timestamp_str)
        except:
            pass
        
        # Try parsing with strptime as fallback
        formats = [
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%d %H:%M:%S'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str.split('+')[0].split('Z')[0], fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse timestamp: {timestamp_str}")

def check_ranking_data():
    """Check and diagnose ranking data issues"""
    db_service = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    
    print("🔍 Checking ranking data...")
    print("=" * 60)
    
    # 1. Check date range of data
    try:
        response = db_service.client.table('ratings_history').select(
            'data_fetched_at'
        ).order('data_fetched_at', desc=True).execute()
        
        if response.data:
            dates = []
            for r in response.data:
                try:
                    date = parse_timestamp(r['data_fetched_at'])
                    dates.append(date)
                except Exception as e:
                    print(f"⚠️  Skipping unparseable date: {r['data_fetched_at']}")
            
            if dates:
                latest_date = max(dates)
                oldest_date = min(dates)
                unique_dates = len(set(d.date() for d in dates))
                
                print(f"📅 Latest data: {latest_date}")
                print(f"📅 Oldest data: {oldest_date}")
                print(f"📅 Days of data: {(latest_date - oldest_date).days}")
                print(f"📅 Unique dates with data: {unique_dates}")
                
                # Check if we have data from ~7 days ago
                seven_days_ago = latest_date - timedelta(days=7)
                has_week_old_data = any(abs((d - seven_days_ago).days) < 1 for d in dates)
                
                if has_week_old_data:
                    print(f"\n✅ Good news! You have data from approximately 7 days ago")
                    print(f"   Rank changes should be working!")
                else:
                    print(f"\n⚠️  WARNING: No data from approximately 7 days ago!")
                    print(f"   This is why all kebabs show as 'NEW'")
                    print(f"   The system needs at least 2 data points to track rank changes")
            else:
                print("❌ Could not parse any dates!")
        else:
            print("❌ No data found in ratings_history table!")
            
    except Exception as e:
        print(f"❌ Error checking dates: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    
    # 2. Test rank change detection for a specific city
    test_city = "Kraków"
    print(f"\n🏙️  Testing rank changes for {test_city}...")
    
    try:
        # Get current rankings
        current_rankings = db_service.get_city_rankings(test_city, limit=5)
        print(f"\n📊 Current top 5 in {test_city}:")
        for kebab in current_rankings:
            print(f"   #{kebab['city_rank']} - {kebab['name']}")
        
        # Get previous rankings
        previous_rankings = db_service.get_previous_rankings(test_city)
        
        if previous_rankings:
            print(f"\n📈 Found {len(previous_rankings)} previous rankings")
            
            # Match and show changes
            for current in current_rankings[:5]:
                prev = next((p for p in previous_rankings 
                           if p['google_place_id'] == current['google_place_id']), None)
                
                if prev:
                    change = prev['city_rank'] - current['city_rank']
                    if change > 0:
                        print(f"   {current['name']}: ↑ {change} places")
                    elif change < 0:
                        print(f"   {current['name']}: ↓ {abs(change)} places")
                    else:
                        print(f"   {current['name']}: → No change")
                else:
                    print(f"   {current['name']}: 🆕 NEW")
        else:
            print("❌ No previous rankings found - this is why everything shows as NEW")
            
    except Exception as e:
        print(f"❌ Error testing rank changes: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    
    # 3. Show sample of timestamp formats in database
    print("\n🔍 Sample timestamp formats in your database:")
    try:
        sample = db_service.client.table('ratings_history').select(
            'data_fetched_at'
        ).limit(5).execute()
        
        for i, record in enumerate(sample.data):
            print(f"   {i+1}. {record['data_fetched_at']}")
            
    except Exception as e:
        print(f"❌ Error getting timestamp samples: {e}")
    
    print("\n" + "=" * 60)
    
    # 4. Suggest solutions
    print("\n💡 SOLUTIONS:")
    print("\n1. Apply the SQL fixes:")
    print("   - Run the SQL code from 'fix_sql_function_types' artifact")
    print("   - This fixes the varchar/text type mismatch")
    
    print("\n2. Update your database.py:")
    print("   - Replace get_previous_rankings method with the fixed version")
    print("   - This handles timestamp parsing issues")
    
    print("\n3. If you have data from multiple dates:")
    print("   - Rank changes should work after applying fixes")
    print("   - If not, check that city_rank values differ between dates")

if __name__ == "__main__":
    check_ranking_data()