# debug_ai.py - Debug AI analysis issues
import os
from dotenv import load_dotenv
from services.database import DatabaseService
from services.google_places_enhanced import GooglePlacesEnhancedService

load_dotenv()

def debug_krakow():
    """Debug why katowice AI analysis isn't working"""
    print("🔍 Debugging katowiceAI Analysis")
    print("=" * 50)
    
    # Check services
    db_service = DatabaseService(
        os.getenv('SUPABASE_URL'), 
        os.getenv('SUPABASE_KEY')
    )
    
    # Get Kraków rankings
    print("\n1. Getting Kkatowice rankings...")
    rankings = db_service.get_city_rankings('katowice')
    print(f"   Found {len(rankings)} kebabs in katowice")
    
    if rankings:
        print("\n2. Top 3 kebabs:")
        for i, kebab in enumerate(rankings[:3]):
            print(f"   #{i+1}: {kebab['name']}")
            print(f"       Google Place ID: {kebab['google_place_id']}")
            print(f"       Score: {kebab['rank_score']}")
            print(f"       Rating: {kebab['rating']} ({kebab['total_reviews']} reviews)")
    
    # Test Google Places API
    print("\n3. Testing Google Places API for reviews...")
    google_service = GooglePlacesEnhancedService(os.getenv('GOOGLE_API_KEY'))
    
    if rankings:
        test_kebab = rankings[0]
        print(f"   Testing reviews for: {test_kebab['name']}")
        try:
            reviews = google_service.get_place_reviews(test_kebab['google_place_id'])
            print(f"   ✅ Found {len(reviews)} reviews")
            if reviews:
                print(f"   Sample review: {reviews[0]['text'][:100]}...")
        except Exception as e:
            print(f"   ❌ Error getting reviews: {e}")
    
    # Check if AI tables exist
    print("\n4. Checking AI tables in database...")
    try:
        result = db_service.client.table('ai_analysis').select('count').execute()
        print("   ✅ ai_analysis table exists")
    except Exception as e:
        print(f"   ❌ ai_analysis table missing: {e}")
        print("   Run the SQL schema in Supabase!")
    
    # Check OpenAI key
    print("\n5. Checking OpenAI API key...")
    if os.getenv('OPENAI_API_KEY'):
        print("   ✅ OpenAI API key found")
    else:
        print("   ❌ OpenAI API key missing!")

if __name__ == "__main__":
    debug_krakow()