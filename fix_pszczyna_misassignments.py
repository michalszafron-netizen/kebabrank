#!/usr/bin/env python3
"""
Script to fix misassigned kebabs in Pszczyna
Moves Kraków kebabs that were incorrectly assigned to Pszczyna back to Kraków
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

def fix_pszczyna_misassignments():
    """Fix kebabs that are in Kraków but assigned to Pszczyna"""
    print("=== FIXING PSZCZYNA MISASSIGNMENTS ===")
    
    # Get Kraków city ID
    krakow_id = db_service.get_city_id('Kraków')
    if not krakow_id:
        print("❌ Could not find Kraków city ID")
        return
    
    # Get Pszczyna city ID
    pszczyna_id = db_service.get_city_id('Pszczyna')
    if not pszczyna_id:
        print("❌ Could not find Pszczyna city ID")
        return
    
    print(f"Kraków ID: {krakow_id}, Pszczyna ID: {pszczyna_id}")
    
    # Find kebabs assigned to Pszczyna that are actually in Kraków
    print("\n🔍 Finding misassigned kebabs...")
    
    # Get all kebabs in Pszczyna
    response = db_service.client.table('kebab_places').select(
        'id, name, address, city_id, google_place_id'
    ).eq('city_id', pszczyna_id).execute()
    
    misassigned_kebabs = []
    
    for kebab in response.data:
        address = kebab.get('address', '').lower()
        
        # Check if address contains Kraków indicators
        krakow_indicators = [
            'kraków', 'krakow', '31-', '31-0', '31-1', '31-2', '31-3', '31-4', '31-5',
            '31-6', '31-7', '31-8', '31-9', 'osiedle', 'ul.', 'aleja', 'plac'
        ]
        
        # Check for Kraków postal codes (31-xxx)
        import re
        krakow_postal_code = re.search(r'31-\d{3}', address)
        
        # Check for Kraków street names and districts
        krakow_districts = [
            'stare miasto', 'kazimierz', 'podgórze', 'nowa huta', 'krowodrza',
            'grzegórzki', 'prądnik', 'zwierzyniec', 'dębniki', 'łagiewniki',
            'bronowice', 'bienczyce', 'prokocim', 'podgórze duchackie'
        ]
        
        is_likely_krakow = (
            krakow_postal_code or
            any(indicator in address for indicator in krakow_indicators) or
            any(district in address for district in krakow_districts) or
            'kraków' in address or 'krakow' in address
        )
        
        if is_likely_krakow:
            misassigned_kebabs.append(kebab)
            print(f"  ⚠️  Misassigned: {kebab['name']}")
            print(f"     Address: {kebab.get('address', 'N/A')}")
    
    if not misassigned_kebabs:
        print("✅ No misassigned kebabs found!")
        return
    
    print(f"\n📊 Found {len(misassigned_kebabs)} misassigned kebabs")
    
    # Fix the assignments
    print("\n🔄 Fixing assignments...")
    fixed_count = 0
    
    for kebab in misassigned_kebabs:
        try:
            # Update the city assignment to Kraków
            db_service.client.table('kebab_places').update({
                'city_id': krakow_id,
                'updated_at': 'now()'
            }).eq('id', kebab['id']).execute()
            
            print(f"  ✅ Fixed: {kebab['name']} → Kraków")
            fixed_count += 1
            
        except Exception as e:
            print(f"  ❌ Error fixing {kebab['name']}: {e}")
    
    print(f"\n🎯 Fixed {fixed_count} out of {len(misassigned_kebabs)} misassigned kebabs")
    
    # Verify the fix
    print("\n🔍 Verifying fix...")
    
    # Check Pszczyna kebabs again
    response_after = db_service.client.table('kebab_places').select(
        'id, name, address, city_id, cities(name)'
    ).eq('cities.name', 'Pszczyna').execute()
    
    print(f"Kebabs remaining in Pszczyna: {len(response_after.data)}")
    
    # Check if any Kraków kebabs are still in Pszczyna
    krakow_in_pszczyna = []
    for kebab in response_after.data:
        address = kebab.get('address', '').lower()
        if 'kraków' in address or 'krakow' in address or '31-' in address:
            krakow_in_pszczyna.append(kebab)
    
    if krakow_in_pszczyna:
        print(f"❌ Still found {len(krakow_in_pszczyna)} Kraków kebabs in Pszczyna:")
        for kebab in krakow_in_pszczyna:
            print(f"  - {kebab['name']}: {kebab.get('address', 'N/A')}")
    else:
        print("✅ All Kraków kebabs have been removed from Pszczyna!")
    
    return fixed_count

def main():
    """Main function"""
    print("=== PSZCZYNA MISASSIGNMENT FIXER ===")
    print("This script will fix kebabs that are in Kraków but assigned to Pszczyna")
    
    # Confirm with user
    response = input("Do you want to proceed? (y/n): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        return
    
    try:
        fixed_count = fix_pszczyna_misassignments()
        
        if fixed_count > 0:
            print(f"\n🎉 Successfully fixed {fixed_count} misassigned kebabs!")
            print("The Pszczyna rankings should now only show actual Pszczyna kebabs.")
        else:
            print("\nℹ️ No misassignments found or fixed.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
