# update_ai_analysis.py - Run AI analysis on kebab reviews
import os
import sys
import argparse
from dotenv import load_dotenv
from services.database import DatabaseService
from services.google_places_enhanced import GooglePlacesEnhancedService
from services.ai_data_updater import AIDataUpdater

load_dotenv()

def update_ai_for_city(city_name: str, limit: int = 10):
    """Update AI analysis for a specific city"""
    print(f"🤖 AI Analysis for {city_name}")
    print("=" * 50)
    
    # Check for OpenAI API key
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        print("Please add: OPENAI_API_KEY=your_openai_api_key")
        return
    
    # Initialize services
    db_service = DatabaseService(
        os.getenv('SUPABASE_URL'), 
        os.getenv('SUPABASE_KEY')
    )
    google_service = GooglePlacesEnhancedService(os.getenv('GOOGLE_API_KEY'))
    ai_updater = AIDataUpdater(db_service, google_service, openai_key)
    
    # Run AI analysis
    try:
        ai_updater.update_ai_analysis_for_city(city_name, limit=limit)
        print("\n✅ AI analysis completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during AI analysis: {e}")
        import traceback
        traceback.print_exc()

def update_all_cities():
    """Update AI analysis for all cities"""
    # Initialize database
    db_service = DatabaseService(
        os.getenv('SUPABASE_URL'), 
        os.getenv('SUPABASE_KEY')
    )
    
    # Get all cities
    cities = db_service.get_cities()
    
    print(f"🌍 Found {len(cities)} cities for AI analysis")
    print("This will analyze top 5 kebabs per city\n")
    
    # Confirm before proceeding
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    # Process each city
    for city in cities:
        update_ai_for_city(city['name'], limit=5)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update AI analysis for kebab rankings')
    parser.add_argument('city', nargs='?', help='City name (e.g., Kraków)')
    parser.add_argument('--limit', type=int, default=10, help='Number of kebabs to analyze per city')
    parser.add_argument('--all', action='store_true', help='Analyze all cities')
    
    args = parser.parse_args()
    
    if args.all:
        update_all_cities()
    elif args.city:
        update_ai_for_city(args.city, args.limit)
    else:
        print("Usage:")
        print("  python update_ai_analysis.py [City Name] [--limit N]")
        print("  python update_ai_analysis.py --all")
        print("\nExamples:")
        print("  python update_ai_analysis.py Kraków")
        print("  python update_ai_analysis.py Warszawa --limit 5")
        print("  python update_ai_analysis.py --all")