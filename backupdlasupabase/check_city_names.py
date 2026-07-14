#!/usr/bin/env python3
"""
Script to check actual city names in the database
"""

import sys
import os
from services.database import DatabaseService
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

if not supabase_url or not supabase_key:
    print('Missing Supabase credentials')
    sys.exit(1)

db_service = DatabaseService(supabase_url, supabase_key)
cities = db_service.get_cities()

print('=== ACTUAL CITY NAMES IN DATABASE ===')
for city in cities:
    if 'Krak' in city['name'] or 'Częstoch' in city['name']:
        print(f"ID: {city['id']}, Name: '{city['name']}'")

# Also check a few more cities to see the pattern
print('\n=== SAMPLE OF CITY NAMES ===')
for city in cities[:10]:
    print(f"ID: {city['id']}, Name: '{city['name']}'")

print('\n=== CHECKING FOR POLISH CHARACTERS ===')
polish_chars = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż']
for city in cities:
    for char in polish_chars:
        if char in city['name'].lower():
            print(f"City with '{char}': '{city['name']}'")
            break
