# update_all_cities.py
import os
import time
from dotenv import load_dotenv
from services.google_places import GooglePlacesService
from services.database import DatabaseService
from services.ranking import RankingService
from services.data_updater import DataUpdater

# Load environment variables
load_dotenv()

# Initialize services
print("Initializing services...")
google_service = GooglePlacesService(os.getenv('GOOGLE_API_KEY'))
db_service = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
ranking_service = RankingService()
data_updater = DataUpdater(google_service, db_service, ranking_service)

# Get all cities
cities = db_service.get_cities()
print(f"\nFound {len(cities)} cities to update")

# Update each city
for i, city in enumerate(cities):
    city_name = city['name']
    print(f"\n[{i+1}/{len(cities)}] Fetching kebab data for {city_name}...")
    
    try:
        data_updater.update_city_data(city_name)
        print(f"✓ Successfully updated {city_name}")
    except Exception as e:
        print(f"✗ Error updating {city_name}: {e}")
    
    # Wait 2 seconds between cities to avoid rate limiting
    if i < len(cities) - 1:
        print("Waiting 2 seconds before next city...")
        time.sleep(2)

print("\n🎉 All done! All cities have been updated.")
print("Check your website now - all cities should have kebab data!")