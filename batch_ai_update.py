# batch_ai_update.py - Process AI analysis in batches
import os
import sys
import time
from dotenv import load_dotenv
from services.database import DatabaseService
from services.google_places_enhanced import GooglePlacesEnhancedService
from services.ai_data_updater import AIDataUpdater

load_dotenv()

def process_cities_batch(city_names, limit=5):
    """Process a batch of cities"""
    # Initialize services
    db_service = DatabaseService(
        os.getenv('SUPABASE_URL'), 
        os.getenv('SUPABASE_KEY')
    )
    google_service = GooglePlacesEnhancedService(os.getenv('GOOGLE_API_KEY'))
    ai_updater = AIDataUpdater(db_service, google_service, os.getenv('OPENAI_API_KEY'))
    
    for city in city_names:
        print(f"\n{'='*50}")
        print(f"Processing: {city}")
        print('='*50)
        try:
            ai_updater.update_ai_analysis_for_city(city, limit=limit)
            print(f"✅ Completed: {city}")
        except Exception as e:
            print(f"❌ Error with {city}: {e}")
        
        # Rate limiting between cities
        time.sleep(5)

# Define city batches
MAJOR_CITIES = [
    'Warszawa', 'Kraków', 'Gdańsk', 'Wrocław', 'Poznań',
    'Katowice', 'Łódź', 'Szczecin', 'Lublin', 'Białystok'
]

MEDIUM_CITIES = [
    'Bydgoszcz', 'Częstochowa', 'Radom', 'Rzeszów', 'Toruń',
    'Sosnowiec', 'Kielce', 'Gliwice', 'Olsztyn', 'Zabrze'
]

SMALLER_CITIES = [
    'Bielsko-Biała', 'Bytom', 'Zielona Góra', 'Rybnik', 'Ruda Śląska',
    'Opole', 'Tychy', 'Gorzów Wielkopolski', 'Elbląg', 'Płock'
]

if __name__ == "__main__":
    print("🤖 Batch AI Analysis Processor")
    print("\nChoose batch to process:")
    print("1. Major cities (10 cities, 10 kebabs each)")
    print("2. Medium cities (10 cities, 5 kebabs each)")
    print("3. Smaller cities (10 cities, 3 kebabs each)")
    print("4. All cities (30 cities)")
    print("5. Custom list")
    
    choice = input("\nEnter choice (1-5): ")
    
    if choice == '1':
        process_cities_batch(MAJOR_CITIES, limit=10)
    elif choice == '2':
        process_cities_batch(MEDIUM_CITIES, limit=5)
    elif choice == '3':
        process_cities_batch(SMALLER_CITIES, limit=3)
    elif choice == '4':
        process_cities_batch(MAJOR_CITIES, limit=10)
        process_cities_batch(MEDIUM_CITIES, limit=5)
        process_cities_batch(SMALLER_CITIES, limit=3)
    elif choice == '5':
        cities = input("Enter city names separated by commas: ").split(',')
        cities = [c.strip() for c in cities]
        limit = int(input("How many kebabs per city? "))
        process_cities_batch(cities, limit=limit)
    
    print("\n✅ Batch processing complete!")