# update_my_cities.py - Update your specific new cities
import os
import time
from dotenv import load_dotenv
from services.google_places import GooglePlacesService
from services.database import DatabaseService
from services.ranking import RankingService
from services.data_updater import DataUpdater

load_dotenv()

# Your new cities
new_cities = [
    
    'Białystok',
    
 
    
]

# Initialize services
google_service = GooglePlacesService(os.getenv('GOOGLE_API_KEY'))
db_service = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
ranking_service = RankingService()
data_updater = DataUpdater(google_service, db_service, ranking_service)

# Update each city
for city in new_cities:
    print(f"\nFetching kebab data for {city}...")
    try:
        data_updater.update_city_data(city)
        print(f"✓ Successfully updated {city}")
    except Exception as e:
        print(f"✗ Error updating {city}: {e}")
    time.sleep(3)  # Rate limiting

print("\n✓ All your cities have been updated!")