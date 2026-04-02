#!/usr/bin/env python3
"""
Comprehensive city mixing detection script for all 62 cities
Detects kebabs assigned to wrong cities based on address analysis
"""

import sys
import os
import json
from datetime import datetime
from services.database import DatabaseService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CityMixingDetector:
    def __init__(self, db_service):
        self.db_service = db_service
        self.cities = []
        self.city_name_to_id = {}
        self.mixing_issues = []
        self.stats = {
            'total_kebabs': 0,
            'total_issues': 0,
            'affected_cities': 0,
            'most_common_mixes': {}
        }
    
    def load_cities(self):
        """Load all cities from database"""
        print("Loading cities from database...")
        self.cities = self.db_service.get_cities()
        self.city_name_to_id = {city['name']: city['id'] for city in self.cities}
        print(f"Loaded {len(self.cities)} cities")
    
    def detect_city_mixing(self):
        """Detect city mixing issues across all cities"""
        print("\n=== DETECTING CITY MIXING ISSUES ===")
        
        # Get all kebabs with their cities
        response = self.db_service.client.table('kebab_places').select(
            'id, name, address, city_id, cities(name)'
        ).execute()
        
        self.stats['total_kebabs'] = len(response.data)
        print(f"Analyzing {self.stats['total_kebabs']} kebabs...")
        
        for kebab in response.data:
            self._analyze_kebab(kebab)
        
        self._calculate_statistics()
        self._generate_report()
    
    def _analyze_kebab(self, kebab):
        """Analyze a single kebab for city mixing issues"""
        address = kebab.get('address', '').lower()
        assigned_city = kebab.get('cities', {}).get('name', 'Unknown')
        kebab_id = kebab['id']
        kebab_name = kebab['name']
        
        # Skip if no address or assigned city
        if not address or assigned_city == 'Unknown':
            return
        
        # Check if address mentions any city that's not the assigned one
        for city_name, city_id in self.city_name_to_id.items():
            city_lower = city_name.lower()
            
            # Skip if it's the same city
            if assigned_city == city_name:
                continue
                
            # Check if city name appears in address
            if city_lower in address:
                # Calculate confidence and check if it's a real issue (not just a street name)
                confidence = self._calculate_confidence(address, city_name, assigned_city)
                
                # Only add if it's not likely a street name
                if confidence != 'low' and not self._is_likely_street_name(address, city_lower, assigned_city):
                    issue = {
                        'kebab_id': kebab_id,
                        'kebab_name': kebab_name,
                        'address': kebab.get('address', ''),
                        'assigned_city': assigned_city,
                        'assigned_city_id': kebab.get('city_id'),
                        'mentioned_city': city_name,
                        'mentioned_city_id': city_id,
                        'confidence': confidence
                    }
                    self.mixing_issues.append(issue)
    
    def _calculate_confidence(self, address, mentioned_city, assigned_city):
        """Calculate confidence level for mixing detection"""
        city_lower = mentioned_city.lower()
        address_lower = address.lower()
        assigned_city_lower = assigned_city.lower()
        
        # Check if it's likely a street name (city name + "ska" or "ska" suffix)
        if self._is_likely_street_name(address, city_lower, assigned_city):
            return 'low'
        
        # Higher confidence if city name appears as standalone word
        if f' {city_lower} ' in address_lower or address_lower.endswith(f' {city_lower}'):
            return 'high'
        elif city_lower in address_lower:
            return 'medium'
        else:
            return 'low'
    
    def _is_likely_street_name(self, address, mentioned_city_lower, assigned_city):
        """Check if the mentioned city is likely just a street name"""
        address_lower = address.lower()
        assigned_city_lower = assigned_city.lower()
        
        # Common street name patterns in Polish addresses
        street_suffixes = ['ska', 'cka', 'owa', 'owa', 'na', 'wa']
        
        # Check if it's a street name pattern (city name + suffix)
        for suffix in street_suffixes:
            street_pattern = f'{mentioned_city_lower}{suffix}'
            if street_pattern in address_lower:
                return True
        
        # Check if it's part of a compound street name
        compound_patterns = [
            f'{mentioned_city_lower} ',
            f' {mentioned_city_lower}',
            f'{mentioned_city_lower}-',
            f'-{mentioned_city_lower}'
        ]
        
        for pattern in compound_patterns:
            if pattern in address_lower:
                # Check if it's not the actual city name at the end of address
                if not address_lower.endswith(f', {assigned_city_lower}'):
                    return True
        
        # Check if it's a common street name like "Wrocławska", "Poznańska", etc.
        common_street_names = [
            'wrocławska', 'poznańska', 'krakowska', 'warszawska', 'gdańska',
            'szczecińska', 'łódzka', 'lubelska', 'katowicka', 'bytomia',
            'gliwicka', 'zabrska', 'rzeszowska', 'olsztyńska', 'białostocka',
            'kielecka', 'toruńska', 'zielonogórska', 'opolska', 'gorzowska',
            'włocławska', 'tarnobrzeska', 'koszalińska', 'kaliska', 'piotrkowska'
        ]
        
        for street_name in common_street_names:
            if street_name in address_lower:
                return True
        
        return False
    
    def _calculate_statistics(self):
        """Calculate comprehensive statistics"""
        self.stats['total_issues'] = len(self.mixing_issues)
        
        # Count affected cities
        affected_cities = set()
        for issue in self.mixing_issues:
            affected_cities.add(issue['assigned_city'])
        self.stats['affected_cities'] = len(affected_cities)
        
        # Count most common mixing patterns
        mixing_patterns = {}
        for issue in self.mixing_issues:
            pattern = f"{issue['mentioned_city']} → {issue['assigned_city']}"
            mixing_patterns[pattern] = mixing_patterns.get(pattern, 0) + 1
        
        # Sort by frequency
        self.stats['most_common_mixes'] = dict(
            sorted(mixing_patterns.items(), key=lambda x: x[1], reverse=True)[:10]
        )
    
    def _generate_report(self):
        """Generate comprehensive detection report"""
        print(f"\n=== CITY MIXING DETECTION REPORT ===")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total kebabs analyzed: {self.stats['total_kebabs']}")
        print(f"Total mixing issues found: {self.stats['total_issues']}")
        print(f"Cities affected: {self.stats['affected_cities']}/{len(self.cities)}")
        
        if self.stats['total_issues'] == 0:
            print("🎉 No city mixing issues detected!")
            return
        
        print(f"\n📊 MOST COMMON MIXING PATTERNS:")
        for pattern, count in self.stats['most_common_mixes'].items():
            print(f"  {pattern}: {count} kebabs")
        
        print(f"\n🏙️ CITY-BY-CITY BREAKDOWN:")
        city_issues = {}
        for issue in self.mixing_issues:
            city = issue['assigned_city']
            city_issues[city] = city_issues.get(city, 0) + 1
        
        for city, count in sorted(city_issues.items(), key=lambda x: x[1], reverse=True):
            print(f"  {city}: {count} issues")
        
        print(f"\n🔍 SAMPLE ISSUES (first 10):")
        for i, issue in enumerate(self.mixing_issues[:10]):
            print(f"  {i+1}. {issue['kebab_name']}")
            print(f"     Address: {issue['address']}")
            print(f"     Assigned to: {issue['assigned_city']}")
            print(f"     Mentions: {issue['mentioned_city']} (confidence: {issue['confidence']})")
            print()
    
    def save_detection_results(self, filename=None):
        """Save detection results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'city_mixing_detection_{timestamp}.json'
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats,
            'issues': self.mixing_issues,
            'cities_analyzed': len(self.cities)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Detection results saved to: {filename}")
        return filename
    
    def get_issues_by_city(self, city_name):
        """Get mixing issues for a specific city"""
        return [issue for issue in self.mixing_issues if issue['assigned_city'] == city_name]
    
    def get_high_confidence_issues(self):
        """Get only high-confidence mixing issues"""
        return [issue for issue in self.mixing_issues if issue['confidence'] == 'high']

def main():
    # Initialize database service
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY environment variables required")
        return
    
    db_service = DatabaseService(supabase_url, supabase_key)
    
    # Create detector and run analysis
    detector = CityMixingDetector(db_service)
    detector.load_cities()
    detector.detect_city_mixing()
    
    # Save results
    results_file = detector.save_detection_results()
    
    # Provide next steps
    if detector.stats['total_issues'] > 0:
        print(f"\n🚀 NEXT STEPS:")
        print(f"1. Review the detection report above")
        print(f"2. Check detailed results in: {results_file}")
        print(f"3. Run: python fix_all_city_mixing.py to fix issues")
        print(f"4. Use: python fix_all_city_mixing.py --city CITY_NAME for specific city")
    else:
        print(f"\n✅ No action needed - database is clean!")

if __name__ == '__main__':
    main()
