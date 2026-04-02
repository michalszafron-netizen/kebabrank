#!/usr/bin/env python3
"""
Comprehensive script to check for city mixing issues across all 62 cities
Identifies kebabs that are assigned to wrong cities based on address analysis
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

# City postal code patterns for major cities
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

# Common street names that might cause confusion
CONFUSING_STREET_NAMES = {
    'Warszawska': 'Warszawa',
    'Krakowska': 'Kraków',
    'Wrocławska': 'Wrocław',
    'Poznańska': 'Poznań',
    'Gdańska': 'Gdańsk',
    'Szczecińska': 'Szczecin',
    'Łódzka': 'Łódź',
    'Lubelska': 'Lublin',
    'Katowicka': 'Katowice',
    'Białostocka': 'Białystok',
    'Gdyńska': 'Gdynia',
    'Częstochowska': 'Częstochowa',
    'Radomska': 'Radom',
    'Sosnowiecka': 'Sosnowiec',
    'Toruńska': 'Toruń',
    'Kielecka': 'Kielce',
    'Rzeszowska': 'Rzeszów',
    'Gliwicka': 'Gliwice',
    'Zabrska': 'Zabrze',
    'Olsztyńska': 'Olsztyn',
    'Bielska': 'Bielsko-Biała',
    'Bytomska': 'Bytom',
    'Zielonogórska': 'Zielona Góra',
    'Rybnicka': 'Rybnik',
    'Rudzka': 'Ruda Śląska',
    'Tyska': 'Tychy',
    'Dąbrowska': 'Dąbrowa Górnicza',
    'Opolska': 'Opole',
    'Elbląska': 'Elbląg',
    'Płocka': 'Płock',
    'Wałbrzyska': 'Wałbrzych',
    'Włocławska': 'Włocławek',
    'Tarnowska': 'Tarnów',
    'Chorzowska': 'Chorzów',
    'Koszalińska': 'Koszalin',
    'Kaliska': 'Kalisz',
    'Legnicka': 'Legnica',
    'Grudziądzka': 'Grudziądz',
    'Jaworznicka': 'Jaworzno',
    'Słupska': 'Słupsk',
    'Jastrzębska': 'Jastrzębie-Zdrój',
    'Sądecka': 'Nowy Sącz',
    'Siedlecka': 'Siedlce',
    'Pilska': 'Piła',
    'Lubińska': 'Lubin',
    'Mysłowicka': 'Mysłowice',
    'Konińska': 'Konin',
    'Piotrkowska': 'Piotrków Trybunalski',
    'Inowrocławska': 'Inowrocław',
    'Pszczyńska': 'Pszczyna',
    'Myszkowska': 'Myszków',
    'Koziegłowska': 'Koziegłowy',
    'Czechowicka': 'Czechowice-Dziedzice',
    'Żarecka': 'Żarki',
    'Jordanecka': 'Jordanów',
    'Zakopiańska': 'Zakopane',
    'Skawińska': 'Skawina',
    'Wielicka': 'Wieliczka',
    'Oświęcimska': 'Oświęcim',
    'Dobczycka': 'Dobczyce'
}

def analyze_city_mixing():
    """Analyze all cities for mixing issues"""
    print("=== COMPREHENSIVE CITY MIXING ANALYSIS ===")
    
    # Get all cities
    cities = db_service.get_cities()
    print(f"Analyzing {len(cities)} cities...")
    
    all_issues = []
    city_stats = {}
    
    for city in cities:
        city_name = city['name']
        city_id = city['id']
        
        print(f"\n🏙️  Analyzing {city_name}...")
        
        # Get all kebabs in this city
        response = db_service.client.table('kebab_places').select(
            'id, name, address, city_id, google_place_id'
        ).eq('city_id', city_id).execute()
        
        issues = []
        
        for kebab in response.data:
            address = kebab.get('address', '').lower()
            kebab_name = kebab['name']
            
            # Check for postal code mismatches
            postal_code_issue = check_postal_code_mismatch(city_name, address, kebab_name)
            if postal_code_issue:
                issues.append(postal_code_issue)
            
            # Check for confusing street names
            street_name_issue = check_confusing_street_name(city_name, address, kebab_name)
            if street_name_issue:
                issues.append(street_name_issue)
            
            # Check for city name mentions in address
            city_mention_issue = check_city_mentions(city_name, address, kebab_name, cities)
            if city_mention_issue:
                issues.append(city_mention_issue)
        
        if issues:
            all_issues.extend(issues)
            city_stats[city_name] = len(issues)
            print(f"  ⚠️  Found {len(issues)} potential issues")
        else:
            print(f"  ✅ No issues found")
    
    # Generate comprehensive report
    generate_report(all_issues, city_stats, len(cities))
    
    return all_issues

def check_postal_code_mismatch(city_name, address, kebab_name):
    """Check if kebab has postal code that doesn't match assigned city"""
    # Extract postal code from address
    postal_match = re.search(r'(\d{2}-\d{3})', address)
    if not postal_match:
        return None
    
    postal_code = postal_match.group(1)
    
    # Check if this postal code matches the expected pattern for the city
    if city_name in CITY_POSTAL_PATTERNS:
        pattern = CITY_POSTAL_PATTERNS[city_name]
        if not re.search(pattern, postal_code):
            # Find which city this postal code belongs to
            actual_city = find_city_by_postal_code(postal_code)
            if actual_city and actual_city != city_name:
                return {
                    'type': 'postal_code_mismatch',
                    'city': city_name,
                    'kebab_name': kebab_name,
                    'address': address,
                    'postal_code': postal_code,
                    'expected_city': actual_city,
                    'severity': 'high'
                }
    
    return None

def find_city_by_postal_code(postal_code):
    """Find which city a postal code belongs to"""
    for city, pattern in CITY_POSTAL_PATTERNS.items():
        if re.search(pattern, postal_code):
            return city
    return None

def check_confusing_street_name(city_name, address, kebab_name):
    """Check if kebab is on a street named after another city"""
    for street_name, street_city in CONFUSING_STREET_NAMES.items():
        street_lower = street_name.lower()
        if street_lower in address and street_city != city_name:
            # Check if it's actually the street name (not the city name)
            if f'ul. {street_lower}' in address or f'ul.{street_lower}' in address or f' {street_lower} ' in address:
                return {
                    'type': 'confusing_street_name',
                    'city': city_name,
                    'kebab_name': kebab_name,
                    'address': address,
                    'street_name': street_name,
                    'street_city': street_city,
                    'severity': 'medium'
                }
    return None

def check_city_mentions(city_name, address, kebab_name, all_cities):
    """Check if address mentions other cities that might indicate misassignment"""
    mentioned_cities = []
    
    for city in all_cities:
        other_city = city['name']
        if other_city != city_name:
            # Check for city name in address (case insensitive)
            if other_city.lower() in address.lower():
                # Make sure it's not just part of a street name
                is_street_name = False
                for street_city in CONFUSING_STREET_NAMES.values():
                    if street_city.lower() in other_city.lower():
                        is_street_name = True
                        break
                
                if not is_street_name:
                    mentioned_cities.append(other_city)
    
    if mentioned_cities:
        return {
            'type': 'city_mention',
            'city': city_name,
            'kebab_name': kebab_name,
            'address': address,
            'mentioned_cities': mentioned_cities,
            'severity': 'low'
        }
    
    return None

def generate_report(issues, city_stats, total_cities):
    """Generate comprehensive analysis report"""
    print("\n" + "="*80)
    print("📊 COMPREHENSIVE CITY MIXING ANALYSIS REPORT")
    print("="*80)
    
    # Overall statistics
    affected_cities = len(city_stats)
    total_issues = len(issues)
    
    print(f"\n📈 OVERALL STATISTICS:")
    print(f"  Total cities analyzed: {total_cities}")
    print(f"  Cities with issues: {affected_cities} ({affected_cities/total_cities*100:.1f}%)")
    print(f"  Total issues found: {total_issues}")
    
    # Cities with most issues
    if city_stats:
        print(f"\n🏆 CITIES WITH MOST ISSUES:")
        sorted_cities = sorted(city_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        for city, count in sorted_cities:
            print(f"  {city}: {count} issues")
    
    # Issue types breakdown
    issue_types = {}
    for issue in issues:
        issue_type = issue['type']
        issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
    
    print(f"\n🔧 ISSUE TYPE BREAKDOWN:")
    for issue_type, count in issue_types.items():
        print(f"  {issue_type}: {count} issues")
    
    # Severity breakdown
    severity_counts = {}
    for issue in issues:
        severity = issue['severity']
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    print(f"\n⚠️  SEVERITY BREAKDOWN:")
    for severity, count in severity_counts.items():
        print(f"  {severity}: {count} issues")
    
    # Sample issues
    print(f"\n🔍 SAMPLE ISSUES (first 10):")
    for i, issue in enumerate(issues[:10]):
        print(f"  {i+1}. {issue['city']}: {issue['kebab_name']}")
        print(f"     Type: {issue['type']}, Severity: {issue['severity']}")
        if issue['type'] == 'postal_code_mismatch':
            print(f"     Postal code: {issue['postal_code']} → Should be in: {issue['expected_city']}")
        elif issue['type'] == 'confusing_street_name':
            print(f"     Street: {issue['street_name']} → Named after: {issue['street_city']}")
        elif issue['type'] == 'city_mention':
            print(f"     Mentions: {', '.join(issue['mentioned_cities'])}")
        print(f"     Address: {issue['address']}")
        print()
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if total_issues > 0:
        print(f"  1. Run the universal fix script to correct all identified issues")
        print(f"  2. Review high-severity issues first (postal code mismatches)")
        print(f"  3. Consider running the Google Places update with enhanced validation")
        print(f"  4. Monitor new data collection to prevent future misassignments")
    else:
        print(f"  ✅ No action needed - database appears clean!")
    
    print(f"\n📁 Next steps:")
    print(f"  - Run: python fix_all_city_mixing.py to fix all identified issues")
    print(f"  - Or run city-specific fixes for targeted corrections")

def main():
    """Main function"""
    print("=== COMPREHENSIVE CITY MIXING CHECKER ===")
    print("This script will analyze all 62 cities for misassigned kebabs")
    
    try:
        issues = analyze_city_mixing()
        
        if issues:
            print(f"\n🎯 Analysis complete! Found {len(issues)} potential issues across all cities.")
            print("Run 'python fix_all_city_mixing.py' to automatically fix these issues.")
        else:
            print(f"\n✅ Analysis complete! No city mixing issues found.")
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
