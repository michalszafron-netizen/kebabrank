#!/usr/bin/env python3
"""
Verify that SEO URL migration works for ALL cities in the database
"""

import requests
from services.database import DatabaseService
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:5000"

def get_all_cities():
    """Get all cities from the database"""
    db = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    cities = db.get_cities()
    return cities

def test_city_redirect(city_name):
    """Test redirect for a specific city"""
    old_url = f"/{city_name.lower().replace(' ', '-')}"
    expected_new_url = f"/kebab-{city_name.lower().replace(' ', '-')}"
    
    try:
        response = requests.get(f"{BASE_URL}{old_url}", allow_redirects=False)
        
        if response.status_code == 301:
            actual_redirect = response.headers.get('Location', '')
            # Handle both relative and absolute URLs
            if actual_redirect == f"{BASE_URL}{expected_new_url}" or actual_redirect == expected_new_url:
                return True, f"✅ {old_url} → {expected_new_url}"
            else:
                return False, f"❌ {old_url} redirected to {actual_redirect} instead of {expected_new_url}"
        else:
            return False, f"❌ {old_url} returned status {response.status_code} instead of 301"
    except Exception as e:
        return False, f"❌ ERROR: {old_url} - {e}"

def test_city_new_url(city_name):
    """Test new SEO URL for a specific city"""
    new_url = f"/kebab-{city_name.lower().replace(' ', '-')}"
    
    try:
        response = requests.get(f"{BASE_URL}{new_url}", allow_redirects=True)
        
        if response.status_code == 200:
            return True, f"✅ {new_url} loads successfully"
        else:
            return False, f"❌ {new_url} returned status {response.status_code}"
    except Exception as e:
        return False, f"❌ ERROR: {new_url} - {e}"

def main():
    print("🔍 Verifying SEO URL Migration for ALL Cities...\n")
    
    # Get all cities from database
    cities = get_all_cities()
    print(f"📊 Found {len(cities)} cities in database\n")
    
    print("🔀 Testing 301 Redirects from old URLs:")
    redirect_results = []
    redirect_messages = []
    
    for city in cities:
        city_name = city['name']
        success, message = test_city_redirect(city_name)
        redirect_results.append(success)
        redirect_messages.append(message)
        if not success:
            print(message)
    
    print("\n🌐 Testing new SEO URLs:")
    new_url_results = []
    new_url_messages = []
    
    for city in cities:
        city_name = city['name']
        success, message = test_city_new_url(city_name)
        new_url_results.append(success)
        new_url_messages.append(message)
        if not success:
            print(message)
    
    # Print summary
    print(f"\n📊 Summary for {len(cities)} cities:")
    print(f"Redirects: {sum(redirect_results)}/{len(redirect_results)} passed")
    print(f"New URLs: {sum(new_url_results)}/{len(new_url_results)} passed")
    
    if all(redirect_results) and all(new_url_results):
        print("\n🎉 ALL CITIES PASSED! SEO URL migration is working correctly for all cities.")
        print("\n📋 First 20 cities verified:")
        for i, city in enumerate(cities[:20]):
            print(f"  {i+1:2d}. {city['name']} → /kebab-{city['name'].lower().replace(' ', '-')}")
        if len(cities) > 20:
            print(f"  ... and {len(cities) - 20} more cities")
    else:
        print("\n⚠️ Some tests failed. Here are the failed tests:")
        for i, (redirect_success, new_url_success) in enumerate(zip(redirect_results, new_url_results)):
            if not redirect_success:
                print(f"  Redirect failed: {redirect_messages[i]}")
            if not new_url_success:
                print(f"  New URL failed: {new_url_messages[i]}")

if __name__ == "__main__":
    main()
