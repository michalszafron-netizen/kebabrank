#!/usr/bin/env python3
"""
Debug script to check cities in database and test specific URLs
"""

import requests
from services.database import DatabaseService
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:5000"

def check_cities():
    """Check what cities exist in database"""
    db = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    cities = db.get_cities()
    
    print("=== DATABASE CITIES ===")
    print(f"Total cities: {len(cities)}")
    print("\nFirst 30 cities:")
    for i, city in enumerate(cities[:30]):
        print(f"  {i+1:2d}. {city['name']}")
    
    # Check specific problematic cities
    test_cities = ['Pszczyna', 'Kraków', 'Warszawa', 'Gdańsk', 'Wrocław']
    print(f"\n=== SPECIFIC CITIES CHECK ===")
    for city_name in test_cities:
        found = [c for c in cities if c['name'].lower() == city_name.lower()]
        print(f"{city_name}: {'FOUND' if found else 'NOT FOUND'}")
        if found:
            print(f"  Database name: {found[0]['name']}")

def test_city_urls():
    """Test specific city URLs"""
    print(f"\n=== TESTING CITY URLS ===")
    
    test_urls = [
        '/kebab-pszczyna',
        '/pszczyna',
        '/kebab-krakow',
        '/krakow',
        '/kebab-warszawa',
        '/warszawa'
    ]
    
    for url in test_urls:
        try:
            response = requests.get(f"{BASE_URL}{url}", allow_redirects=False)
            print(f"\n{url}:")
            print(f"  Status: {response.status_code}")
            if response.status_code == 301:
                print(f"  Redirects to: {response.headers.get('Location')}")
            elif response.status_code == 200:
                print(f"  Loads successfully")
            else:
                print(f"  Other status")
        except Exception as e:
            print(f"\n{url}: ERROR - {e}")

def debug_city_matching():
    """Debug the city matching logic"""
    print(f"\n=== DEBUG CITY MATCHING ===")
    
    db = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    cities = db.get_cities()
    
    test_slugs = ['pszczyna', 'krakow', 'warszawa', 'gdansk', 'wroclaw']
    
    for slug in test_slugs:
        print(f"\nTesting slug: {slug}")
        
        # Simulate the city matching logic
        city_mapping = {}
        for city in cities:
            city_name = city['name']
            
            # Basic slug (spaces to hyphens, lowercase)
            basic_slug = city_name.lower().replace(' ', '-')
            city_mapping[basic_slug] = city_name
            
            # Handle Polish characters properly
            polish_mapping = {
                'ł': 'l', 'ó': 'o', 'ą': 'a', 'ę': 'e', 'ć': 'c', 
                'ń': 'n', 'ś': 's', 'ź': 'z', 'ż': 'z'
            }
            
            # Create slug with Polish characters replaced
            polish_slug = city_name.lower()
            for polish_char, replacement in polish_mapping.items():
                polish_slug = polish_slug.replace(polish_char, replacement)
            polish_slug = polish_slug.replace(' ', '-')
            city_mapping[polish_slug] = city_name
            
            # Also handle direct city names (without slugification)
            city_mapping[city_name.lower()] = city_name
        
        if slug in city_mapping:
            print(f"  ✅ MATCH FOUND: {slug} -> {city_mapping[slug]}")
        else:
            print(f"  ❌ NO MATCH for {slug}")
            print(f"  Available slugs: {list(city_mapping.keys())[:10]}...")

if __name__ == "__main__":
    check_cities()
    test_city_urls()
    debug_city_matching()
