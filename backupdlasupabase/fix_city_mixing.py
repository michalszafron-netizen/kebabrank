#!/usr/bin/env python3
"""
Script to fix city mixing issues where kebabs from Kraków appear in Pszczyna
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
    
    print('=== FIXING CITY MIXING ISSUES ===')
    
    # Get city IDs
    krakow_id = db_service.get_city_id('Kraków')
    pszczyna_id = db_service.get_city_id('Pszczyna')
    
    print(f'Kraków city ID: {krakow_id}')
    print(f'Pszczyna city ID: {pszczyna_id}')
    
    if not krakow_id or not pszczyna_id:
        print("Error: Could not find city IDs")
        return
    
    # Find kebabs with Kraków addresses assigned to Pszczyna
    print('\n1. Finding kebabs with incorrect city assignments...')
    
    response = db_service.client.table('kebab_places').select('id, name, address, city_id').execute()
    kebabs_to_fix = []
    
    for kebab in response.data:
        address = kebab.get('address', '')
        city_id = kebab.get('city_id')
        
        # Check if address contains Kraków but city_id is Pszczyna
        if 'Kraków' in address and city_id == pszczyna_id:
            kebabs_to_fix.append(kebab)
    
    print(f'Found {len(kebabs_to_fix)} kebabs with incorrect city assignments:')
    for kebab in kebabs_to_fix:
        print(f'  - {kebab["name"]}: {kebab["address"]}')
        print(f'    Currently assigned to Pszczyna (ID: {pszczyna_id})')
        print(f'    Should be assigned to Kraków (ID: {krakow_id})')
    
    if not kebabs_to_fix:
        print('No city mixing issues found!')
        return
    
    # Ask for confirmation before making changes
    print(f'\n2. Ready to fix {len(kebabs_to_fix)} kebabs.')
    confirmation = input('Do you want to proceed with fixing these assignments? (y/n): ')
    
    if confirmation.lower() != 'y':
        print('Fix cancelled.')
        return
    
    # Fix the city assignments
    print('\n3. Fixing city assignments...')
    
    fixed_count = 0
    for kebab in kebabs_to_fix:
        try:
            # Update the kebab place to assign it to Kraków
            result = db_service.client.table('kebab_places').update({
                'city_id': krakow_id,
                'updated_at': 'now()'
            }).eq('id', kebab['id']).execute()
            
            if result.data:
                print(f'✓ Fixed: {kebab["name"]} -> Kraków')
                fixed_count += 1
            else:
                print(f'✗ Failed to fix: {kebab["name"]}')
                
        except Exception as e:
            print(f'✗ Error fixing {kebab["name"]}: {e}')
    
    print(f'\n4. Fix completed: {fixed_count}/{len(kebabs_to_fix)} kebabs fixed')
    
    # Verify the fix
    print('\n5. Verifying the fix...')
    
    # Check Pszczyna kebabs after fix
    response = db_service.client.table('kebab_places').select('id, name, address, city_id').eq('city_id', pszczyna_id).execute()
    print(f'Kebabs remaining in Pszczyna: {len(response.data)}')
    
    # Check for any remaining Kraków addresses in Pszczyna
    remaining_issues = []
    for kebab in response.data:
        if 'Kraków' in kebab.get('address', ''):
            remaining_issues.append(kebab)
    
    if remaining_issues:
        print(f'WARNING: Still found {len(remaining_issues)} kebabs with Kraków addresses in Pszczyna:')
        for kebab in remaining_issues:
            print(f'  - {kebab["name"]}: {kebab["address"]}')
    else:
        print('✓ No remaining city mixing issues found!')
    
    print('\n=== FIX COMPLETE ===')

if __name__ == '__main__':
    main()
