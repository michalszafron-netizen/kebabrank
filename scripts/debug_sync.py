import os
import sys
import requests
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.database import DatabaseService
from services.google_places import GooglePlacesService

def test_specific_photo(place_id):
    load_dotenv()
    db_service = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    google_service = GooglePlacesService(os.getenv('GOOGLE_API_KEY'))
    
    print(f"🔍 Testing Place ID: {place_id}")
    
    # 1. Get current state
    res = db_service.client.table('kebab_places').select('name, photo_url').eq('id', place_id).execute()
    if not res.data:
        print("❌ Place not found.")
        return
    
    place = res.data[0]
    print(f"📝 Name: {place['name']}")
    print(f"🔗 Current photo_url: {place['photo_url'][:50]}...")
    
    photo_ref = place['photo_url']
    if not photo_ref or photo_ref == 'NONE' or photo_ref.startswith('http'):
        print("⏭️ Already synced or NONE. Nothing to test.")
        return

    # 2. Try download from Google
    try:
        print("📥 Downloading from Google...")
        photo_response = google_service.gmaps.places_photo(
            photo_reference=photo_ref,
            max_width=400
        )
        
        image_data = b''
        for chunk in photo_response:
            image_data += chunk
            
        print(f"✅ Downloaded {len(image_data)} bytes.")
        
    except Exception as e:
        print(f"❌ GOOGLE DOWNLOAD FAILED: {e}")

if __name__ == "__main__":
    # Test "Baku Kebab & Grill" in Warsaw (ID 2239 from my previous query)
    test_specific_photo(2239)
