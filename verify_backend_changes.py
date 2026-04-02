#!/usr/bin/env python3
"""
Verification script for Phase 1 backend implementation
"""

from services.database import DatabaseService
import os
from dotenv import load_dotenv

def verify_coordinate_integration():
    """Verify that coordinates are properly integrated into the backend"""
    print("=== Phase 1 Backend Implementation Verification ===\n")
    
    # Load environment and connect to database
    load_dotenv()
    db = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    
    # Test 1: Verify database has coordinate data
    print("1. Testing database coordinate data...")
    response = db.client.table('kebab_places').select('name, latitude, longitude').limit(3).execute()
    
    if response.data:
        print("✅ Database contains coordinate data:")
        for place in response.data:
            print(f"   {place['name']}: lat={place.get('latitude')}, lng={place.get('longitude')}")
    else:
        print("❌ No data found in database")
        return False
    
    # Test 2: Verify get_city_rankings returns coordinates
    print("\n2. Testing get_city_rankings method...")
    rankings = db.get_city_rankings('Warszawa', limit=2)
    
    if rankings:
        print("✅ City rankings method returns data")
        for kebab in rankings:
            has_lat = 'latitude' in kebab and kebab['latitude'] is not None
            has_lng = 'longitude' in kebab and kebab['longitude'] is not None
            print(f"   {kebab['name']}: lat={has_lat}, lng={has_lng}")
            
            if not (has_lat and has_lng):
                print("❌ Missing coordinates in rankings response")
                return False
    else:
        print("❌ No rankings data returned")
        return False
    
    # Test 3: Verify get_global_rankings returns coordinates
    print("\n3. Testing get_global_rankings method...")
    global_rankings = db.get_global_rankings(limit=2)
    
    if global_rankings:
        print("✅ Global rankings method returns data")
        for kebab in global_rankings:
            has_lat = 'latitude' in kebab and kebab['latitude'] is not None
            has_lng = 'longitude' in kebab and kebab['longitude'] is not None
            print(f"   {kebab['name']}: lat={has_lat}, lng={has_lng}")
            
            if not (has_lat and has_lng):
                print("❌ Missing coordinates in global rankings response")
                return False
    else:
        print("❌ No global rankings data returned")
        return False
    
    # Test 4: Check data quality
    print("\n4. Checking data quality...")
    all_places = db.client.table('kebab_places').select('latitude, longitude').execute()
    
    valid_coords = 0
    invalid_coords = 0
    
    for place in all_places.data:
        lat = place.get('latitude')
        lng = place.get('longitude')
        
        if lat is not None and lng is not None:
            try:
                # Check if coordinates are valid numbers
                float(lat)
                float(lng)
                valid_coords += 1
            except (ValueError, TypeError):
                invalid_coords += 1
        else:
            invalid_coords += 1
    
    print(f"   Valid coordinates: {valid_coords}")
    print(f"   Invalid/missing coordinates: {invalid_coords}")
    
    if valid_coords > 0:
        print("✅ Valid coordinate data found")
    else:
        print("❌ No valid coordinate data found")
        return False
    
    print("\n🎉 Phase 1 Backend Implementation: SUCCESS!")
    print("Coordinates are properly integrated into the database and API methods.")
    return True

if __name__ == '__main__':
    try:
        success = verify_coordinate_integration()
        if success:
            print("\n✅ Ready to proceed with Phase 2: Frontend Map Integration")
        else:
            print("\n❌ Backend implementation needs fixes before proceeding")
    except Exception as e:
        print(f"❌ Verification failed with error: {e}")
        import traceback
        traceback.print_exc()
