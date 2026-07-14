#!/usr/bin/env python3
"""
Script to investigate why Pszczyna is showing kebabs from Kraków
"""

import sys
import os
from services.database import DatabaseService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Initialize database service
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY environment variables required")
        return
    
    db_service = DatabaseService(supabase_url, supabase_key)
    
    print('=== INVESTIGATING PSZCZYNA DATA ISSUE ===')
    
    # Check Pszczyna city ID and kebabs
    print('\n1. Checking Pszczyna city data:')
    pszczyna_id = db_service.get_city_id('Pszczyna')
    print(f'Pszczyna city ID: {pszczyna_id}')
    
    if not pszczyna_id:
        print("Pszczyna city not found in database!")
        return
    
    # Get kebabs assigned to Pszczyna
    response = db_service.client.table('kebab_places').select('id, name, address, city_id').eq('city_id', pszczyna_id).execute()
    print(f'Kebabs in Pszczyna: {len(response.data)}')
    for kebab in response.data:
        print(f'  - {kebab["name"]} (ID: {kebab["id"]})')
        print(f'    Address: {kebab.get("address", "No address")}')
    
    # Check if there are kebabs with wrong city assignments
    print('\n2. Checking for kebabs with Kraków addresses in Pszczyna:')
    response = db_service.client.table('kebab_places').select('id, name, address, city_id').execute()
    krakow_in_pszczyna = []
    
    for kebab in response.data:
        address = kebab.get('address', '')
        city_id = kebab.get('city_id')
        
        # Check if address contains Kraków but city_id is Pszczyna
        if 'Kraków' in address and city_id == pszczyna_id:
            krakow_in_pszczyna.append(kebab)
    
    print(f'Found {len(krakow_in_pszczyna)} kebabs with Kraków addresses assigned to Pszczyna:')
    for kebab in krakow_in_pszczyna:
        print(f'  - {kebab["name"]}: {kebab["address"]}')
    
    # Check the actual rankings for Pszczyna
    print('\n3. Testing Pszczyna rankings:')
    rankings = db_service.get_city_rankings('Pszczyna', limit=20)
    print(f'Total rankings returned: {len(rankings)}')
    
    for i, kebab in enumerate(rankings[:10]):
        print(f'  {i+1}. {kebab["name"]} - {kebab.get("address", "No address")}')
    
    # Check if there's a city mixing issue in the database
    print('\n4. Checking for city assignment issues:')
    
    # Get all kebabs and their cities
    response = db_service.client.table('kebab_places').select('id, name, address, city_id, cities(name)').execute()
    
    city_mixing_issues = []
    for kebab in response.data:
        address = kebab.get('address', '')
        city_name = kebab.get('cities', {}).get('name', 'Unknown')
        
        # Check if address mentions a different city than assigned
        if 'Kraków' in address and city_name != 'Kraków':
            city_mixing_issues.append({
                'kebab_name': kebab['name'],
                'address': address,
                'assigned_city': city_name,
                'mentioned_city': 'Kraków'
            })
    
    print(f'Found {len(city_mixing_issues)} city mixing issues:')
    for issue in city_mixing_issues:
        print(f'  - {issue["kebab_name"]}')
        print(f'    Address: {issue["address"]}')
        print(f'    Assigned to: {issue["assigned_city"]}')
        print(f'    Mentions: {issue["mentioned_city"]}')
    
    print('\n=== INVESTIGATION COMPLETE ===')

if __name__ == '__main__':
    main()
