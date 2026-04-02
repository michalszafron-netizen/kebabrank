# force_refresh.py
import sys
import os
from datetime import datetime
from dotenv import load_dotenv
from services.database import DatabaseService
from services.data_updater import DataUpdater
from services.google_places import GooglePlacesService
from services.ranking import RankingService

load_dotenv()

def force_refresh_city(city_name):
    """Force refresh rankings for a city"""
    print(f"🔄 Force refreshing {city_name}...")
    
    db_service = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    google_service = GooglePlacesService(os.getenv('GOOGLE_API_KEY'))
    ranking_service = RankingService()
    data_updater = DataUpdater(google_service, db_service, ranking_service)
    
    # Force update
    data_updater.update_city_data(city_name)
    
    # Recalculate rankings
    city_id = db_service.get_city_id(city_name)
    if city_id:
        db_service.recalculate_city_rankings(city_id)
        print(f"✅ {city_name} refreshed successfully!")
    else:
        print(f"❌ City {city_name} not found!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        city_name = ' '.join(sys.argv[1:])
        force_refresh_city(city_name)
    else:
        print("Usage: python force_refresh.py [City Name]")