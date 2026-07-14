#!/usr/bin/env python3
"""
Universal script to fix all city mixing issues identified by check_all_city_mixing.py
Automatically corrects misassigned kebabs based on postal code and address analysis
"""

import sys
import os
import re
from services.database import DatabaseService
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

if not supabase_url or not supabase_key:
    print('Missing Supabase credentials')
    sys.exit(1)

db_service = DatabaseService(supabase_url, supabase_key)

# City postal code patterns for major cities (same as in check script)
CITY_POSTAL_PATTERNS = {
    'Warszawa': r'00-\d{3}|01-\d{3}|02-\d{3}|03-\d{3}|04-\d{3}|05-\d{3}',
    'Kraków': r'30-\d{3}|31-\d{3}',
    'Wrocław': r'50-\d{3}|51-\d{3}|52-\d{3}|53-\d{3}|54-\d{3}',
    'Poznań': r'60-\d{3}|61-\d{3}',
    'Gdańsk': r'80-\d{3}',
    'Szczecin': r'70-\d{3}|71-\d{3}',
    'Łódź': r'90-\d{3}|91-\d{3}|92-\d{3}|93-\d{3}|94-\d{3}',
    'Lublin': r'20-\d{3}',
    'Katowice': r'40-\d{3}|41-\d{3}',
    'Białystok': r'15-\d{3}|16-\d{3}',
    'Gdynia': r'81-\d{3}',
    'Częstochowa': r'42-\d{3}',
    'Radom': r'26-\d{3}',
    'Sosnowiec': r'41-\d{3}',
    'Toruń': r'87-\d{3}',
    'Kielce': r'25-\d{3}',
    'Rzeszów': r'35-\d{3}',
    'Gliwice': r'44-\d{3}',
    'Zabrze': r'41-\d{3}',
    'Olsztyn': r'10-\d{3}',
    'Bielsko-Biała': r'43-\d{3}',
    'Bytom': r'41-\d{3}',
    'Zielona Góra': r'65-\d{3}|66-\d{3}',
    'Rybnik': r'44-\d{3}',
    'Ruda Śląska': r'41-\d{3}',
    'Tychy': r'43-\d{3}',
    'Dąbrowa Górnicza': r'41-\d{3}',
    'Opole': r'45-\d{3}|46-\d{3}',
    'Elbląg': r'82-\d{3}',
    'Płock': r'09-\d{3}',
    'Wałbrzych': r'58-\d{3}',
    'Włocławek': r'87-\d{3}',
    'Tarnów': r'33-\d{3}',
    'Chorzów': r'41-\d{3}',
    'Koszalin': r'75-\d{3}|76-\d{3}',
    'Kalisz': r'62-\d{3}',
    'Legnica': r'59-\d{3}',
    'Grudziądz': r'86-\d{3}',
    'Jaworzno': r'43-\d{3}',
    'Słupsk': r'76-\d{3}',
    'Jastrzębie-Zdrój': r'44-\d{3}',
    'Nowy Sącz': r'33-\d{3}',
    'Siedlce': r'08-\d{3}',
    'Piła': r'64-\d{3}',
    'Lubin': r'59-\d{3}',
    'Mysłowice': r'41-\d{3}',
    'Konin': r'62-\d{3}',
    'Piotrków Trybunalski': r'97-\d{3}',
    'Inowrocław': r'88-\d{3}',
    'Pszczyna': r'43-\d{3}',
    'Myszków': r'42-\d{3}',
    'Koziegłowy': r'42-\d{3}',
    'Czechowice-Dziedzice': r'43-\d{3}',
    'Żarki': r'42-\d{3}',
    'Jordanów': r'34-\d{3}',
    'Zakopane': r'34-\d{3}',
    'Skawina': r'32-\d{3}',
    'Wieliczka': r'32-\d{3}',
    'Oświęcim': r'32-\d{3}',
    'Dobczyce': r'32-\d{3}'
}

def find_city_by_postal_code(postal_code):
    """Find which city a postal code belongs to"""
    for city, pattern in CITY_POSTAL_PATTERNS.items():
        if re.search(pattern, postal_code):
            return city
    return None

def fix_all_city_mixing():
    """Fix all identified city mixing issues"""
    print("=== UNIVERSAL CITY MIXING FIXER ===")
    
    # Get all cities
    cities = db_service.get_cities()
    print(f"Processing {len(cities)} cities...")
    
    total_fixed = 0
    city_fixes = {}
    
    for city in cities:
        city_name = city['name']
        city_id = city['id']
        
        print(f"\n🏙️  Processing {city_name}...")
        
        # Get all kebabs in this city
        response = db_service.client.table('kebab_places').select(
            'id, name, address, city_id, google_place_id'
        ).eq('city_id', city_id).execute()
        
        fixed_in_city = 0
        
        for kebab in response.data:
            address = kebab.get('address', '')
            kebab_name = kebab['name']
            kebab_id = kebab['id']
            
            # Extract postal code from address
            postal_match = re.search(r'(\d{2}-\d{3})', address)
            if not postal_match:
                continue
            
            postal_code = postal_match.group(1)
            
            # Check if this postal code matches the expected pattern for the city
            if city_name in CITY_POSTAL_PATTERNS:
                pattern = CITY_POSTAL_PATTERNS[city_name]
                if not re.search(pattern, postal_code):
                    # Find which city this postal code belongs to
                    actual_city = find_city_by_postal_code(postal_code)
                    if actual_city and actual_city != city_name:
                        # Get the correct city ID
                        actual_city_id = db_service.get_city_id(actual_city)
                        if actual_city_id:
                            try:
                                # Update the city assignment
                                db_service.client.table('kebab_places').update({
                                    'city_id': actual_city_id,
                                    'updated_at': 'now()'
                                }).eq('id', kebab_id).execute()
                                
                                print(f"  ✅ Fixed: {kebab_name}")
                                print(f"     From: {city_name} → To: {actual_city}")
                                print(f"     Postal code: {postal_code}")
                                print(f"     Address: {address}")
                                
                                fixed_in_city += 1
                                total_fixed += 1
                                
                            except Exception as e:
                                print(f"  ❌ Error fixing {kebab_name}: {e}")
        
        if fixed_in_city > 0:
            city_fixes[city_name] = fixed_in_city
            print(f"  📊 Fixed {fixed_in_city} kebabs in {city_name}")
        else:
            print(f"  ✅ No fixes needed in {city_name}")
    
    # Generate summary report
    generate_fix_report(total_fixed, city_fixes, len(cities))
    
    return total_fixed

def generate_fix_report(total_fixed, city_fixes, total_cities):
    """Generate comprehensive fix report"""
    print("\n" + "="*80)
    print("📊 UNIVERSAL CITY MIXING FIX REPORT")
    print("="*80)
    
    affected_cities = len(city_fixes)
    
    print(f"\n📈 FIX SUMMARY:")
    print(f"  Total cities processed: {total_cities}")
    print(f"  Cities with fixes applied: {affected_cities} ({affected_cities/total_cities*100:.1f}%)")
    print(f"  Total kebabs fixed: {total_fixed}")
    
    if city_fixes:
        print(f"\n🏆 CITIES WITH MOST FIXES:")
        sorted_cities = sorted(city_fixes.items(), key=lambda x: x[1], reverse=True)[:10]
        for city, count in sorted_cities:
            print(f"  {city}: {count} kebabs fixed")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if total_fixed > 0:
        print(f"  1. ✅ Database has been cleaned up successfully!")
        print(f"  2. 🔄 Consider running the Google Places update with enhanced validation")
        print(f"  3. 📊 Monitor new data collection to prevent future misassignments")
        print(f"  4. 🧪 Test the website to ensure all cities show correct kebabs")
    else:
        print(f"  ✅ No fixes needed - database was already clean!")
    
    print(f"\n🎯 Next steps:")
    print(f"  - Run the website to verify all cities show correct kebabs")
    print(f"  - Consider running 'python update_all_cities.py' with enhanced validation")
    print(f"  - Monitor new data collection to maintain data quality")

def main():
    """Main function"""
    print("=== UNIVERSAL CITY MIXING FIXER ===")
    print("This script will fix all identified city mixing issues")
    print("WARNING: This will modify the database. Make sure you have a backup!")
    
    # Confirm with user
    response = input("Do you want to proceed? (y/n): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        return
    
    try:
        total_fixed = fix_all_city_mixing()
        
        if total_fixed > 0:
            print(f"\n🎉 Successfully fixed {total_fixed} misassigned kebabs!")
            print("The database has been cleaned up and all cities should now show correct kebabs.")
        else:
            print(f"\nℹ️ No misassignments found or fixed - database was already clean!")
            
    except Exception as e:
        print(f"❌ Error during fixing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
