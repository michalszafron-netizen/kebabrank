#!/usr/bin/env python3
"""
Script to check the Pszczyna city mixing issue
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

# Check Pszczyna specifically
print('=== CHECKING PSZCZYNA KEBABS ===')
response = db_service.client.table('kebab_places').select(
    'id, name, address, city_id, cities(name)'
).eq('cities.name', 'Pszczyna').execute()

print(f'Found {len(response.data)} kebabs in Pszczyna:')
for kebab in response.data:
    print(f'  - {kebab["name"]}')
    print(f'    Address: {kebab.get("address", "N/A")}')
    cities_data = kebab.get("cities")
    if cities_data:
        print(f'    City: {cities_data.get("name", "Unknown")}')
    else:
        print(f'    City: Unknown (no city data)')
    print()

# Also check if there are kebabs that should be in Pszczyna but aren't
print('=== CHECKING FOR KRAKÓW KEBABS THAT MENTION PSZCZYNA ===')
response2 = db_service.client.table('kebab_places').select(
    'id, name, address, city_id, cities(name)'
).eq('cities.name', 'Kraków').execute()

pszczyna_mentions = []
for kebab in response2.data:
    address = kebab.get('address', '').lower()
    if 'pszczyna' in address:
        pszczyna_mentions.append(kebab)

print(f'Found {len(pszczyna_mentions)} Kraków kebabs mentioning Pszczyna:')
for kebab in pszczyna_mentions:
    print(f'  - {kebab["name"]}')
    print(f'    Address: {kebab.get("address", "N/A")}')
    print()

# Check if there are kebabs in other cities that should be in Pszczyna
print('=== CHECKING FOR OTHER CITIES WITH PSZCZYNA MENTIONS ===')
response3 = db_service.client.table('kebab_places').select(
    'id, name, address, city_id, cities(name)'
).execute()

pszczyna_issues = []
for kebab in response3.data:
    address = kebab.get('address', '').lower()
    current_city = kebab.get('cities', {}).get('name', 'Unknown')
    
    if 'pszczyna' in address and current_city != 'Pszczyna':
        pszczyna_issues.append(kebab)

print(f'Found {len(pszczyna_issues)} kebabs that mention Pszczyna but are in wrong cities:')
for kebab in pszczyna_issues:
    print(f'  - {kebab["name"]}')
    print(f'    Address: {kebab.get("address", "N/A")}')
    print(f'    Current City: {kebab.get("cities", {}).get("name", "Unknown")}')
    print()
