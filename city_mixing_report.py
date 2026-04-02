#!/usr/bin/env python3
"""
City mixing analytics and reporting script
Generates comprehensive reports and visualizations of mixing issues
"""

import sys
import os
import json
import argparse
from datetime import datetime
from collections import Counter

class CityMixingReporter:
    def __init__(self):
        self.detection_data = None
        self.fix_data = None
    
    def load_data(self, detection_file=None, fix_file=None):
        """Load detection and fix data from JSON files"""
        # Load detection data
        if detection_file:
            try:
                with open(detection_file, 'r', encoding='utf-8') as f:
                    self.detection_data = json.load(f)
                print(f"✅ Loaded detection data from: {detection_file}")
            except Exception as e:
                print(f"❌ Error loading detection data: {e}")
                return False
        
        # Load fix data
        if fix_file:
            try:
                with open(fix_file, 'r', encoding='utf-8') as f:
                    self.fix_data = json.load(f)
                print(f"✅ Loaded fix data from: {fix_file}")
            except Exception as e:
                print(f"❌ Error loading fix data: {e}")
        
        return True
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        if not self.detection_data:
            print("❌ No detection data loaded")
            return
        
        print("\n" + "="*80)
        print("📊 CITY MIXING COMPREHENSIVE REPORT")
        print("="*80)
        
        stats = self.detection_data['stats']
        issues = self.detection_data['issues']
        
        # Basic statistics
        print(f"\n📈 BASIC STATISTICS")
        print(f"  Total kebabs analyzed: {stats['total_kebabs']:,}")
        print(f"  Total mixing issues found: {stats['total_issues']:,}")
        print(f"  Cities affected: {stats['affected_cities']:,}/{stats.get('cities_analyzed', '?')}")
        print(f"  Issue rate: {(stats['total_issues']/stats['total_kebabs']*100):.1f}%")
        
        # Confidence breakdown
        confidence_counts = Counter(issue['confidence'] for issue in issues)
        print(f"\n🎯 CONFIDENCE BREAKDOWN")
        for confidence, count in confidence_counts.most_common():
            percentage = (count / len(issues)) * 100
            print(f"  {confidence.title()}: {count:,} issues ({percentage:.1f}%)")
        
        # Top mixing patterns
        print(f"\n🔀 TOP 10 MIXING PATTERNS")
        for pattern, count in stats['most_common_mixes'].items():
            percentage = (count / len(issues)) * 100
            print(f"  {pattern}: {count:,} issues ({percentage:.1f}%)")
        
        # Most affected cities
        city_issues = Counter(issue['assigned_city'] for issue in issues)
        print(f"\n🏙️ MOST AFFECTED CITIES (Top 10)")
        for city, count in city_issues.most_common(10):
            percentage = (count / len(issues)) * 100
            print(f"  {city}: {count:,} issues ({percentage:.1f}%)")
        
        # Fix results if available
        if self.fix_data:
            self._include_fix_results()
    
    def _include_fix_results(self):
        """Include fix results in the report"""
        print(f"\n🛠️ FIXING RESULTS")
        print(f"  Issues fixed: {self.fix_data['issues_fixed']:,}")
        print(f"  Issues skipped: {self.fix_data['issues_skipped']:,}")
        print(f"  Errors encountered: {len(self.fix_data['errors'])}")
        
        if self.fix_data['backup_file']:
            print(f"  Backup created: {self.fix_data['backup_file']}")
    
    def generate_city_report(self, city_name):
        """Generate detailed report for a specific city"""
        if not self.detection_data:
            print("❌ No detection data loaded")
            return
        
        city_issues = [issue for issue in self.detection_data['issues'] 
                      if issue['assigned_city'] == city_name]
        
        if not city_issues:
            print(f"❌ No issues found for city: {city_name}")
            return
        
        print(f"\n" + "="*80)
        print(f"🏙️ DETAILED REPORT FOR: {city_name}")
        print("="*80)
        
        print(f"\n📊 CITY STATISTICS")
        print(f"  Total issues: {len(city_issues):,}")
        
        # Confidence breakdown for this city
        confidence_counts = Counter(issue['confidence'] for issue in city_issues)
        for confidence, count in confidence_counts.most_common():
            percentage = (count / len(city_issues)) * 100
            print(f"  {confidence.title()} confidence: {count:,} issues ({percentage:.1f}%)")
        
        # Where are kebabs coming from?
        source_cities = Counter(issue['mentioned_city'] for issue in city_issues)
        print(f"\n🔀 SOURCE CITIES (Where kebabs should be assigned)")
        for source_city, count in source_cities.most_common(5):
            percentage = (count / len(city_issues)) * 100
            print(f"  {source_city}: {count:,} kebabs ({percentage:.1f}%)")
        
        # Sample issues
        print(f"\n🔍 SAMPLE ISSUES (First 5)")
        for i, issue in enumerate(city_issues[:5]):
            print(f"  {i+1}. {issue['kebab_name']}")
            print(f"     Address: {issue['address']}")
            print(f"     Should be in: {issue['mentioned_city']}")
            print(f"     Confidence: {issue['confidence']}")
            print()
    
    def generate_pattern_report(self):
        """Generate report on mixing patterns"""
        if not self.detection_data:
            print("❌ No detection data loaded")
            return
        
        issues = self.detection_data['issues']
        
        # Analyze patterns
        patterns = Counter(f"{issue['mentioned_city']} → {issue['assigned_city']}" 
                          for issue in issues)
        
        print(f"\n" + "="*80)
        print(f"🔀 MIXING PATTERN ANALYSIS")
        print("="*80)
        
        print(f"\n📊 PATTERN FREQUENCIES")
        for pattern, count in patterns.most_common(15):
            percentage = (count / len(issues)) * 100
            print(f"  {pattern}: {count:,} issues ({percentage:.1f}%)")
        
        # Analyze directionality
        print(f"\n🔄 DIRECTIONAL ANALYSIS")
        directional_patterns = {}
        for issue in issues:
            key = (issue['mentioned_city'], issue['assigned_city'])
            directional_patterns[key] = directional_patterns.get(key, 0) + 1
        
        # Find bidirectional mixing
        bidirectional = []
        for (city_a, city_b), count_ab in directional_patterns.items():
            reverse_key = (city_b, city_a)
            if reverse_key in directional_patterns:
                count_ba = directional_patterns[reverse_key]
                if count_ab + count_ba >= 5:  # Only show significant pairs
                    bidirectional.append((city_a, city_b, count_ab, count_ba))
        
        if bidirectional:
            print(f"\n🔄 BIDIRECTIONAL MIXING PATTERNS")
            for city_a, city_b, count_ab, count_ba in sorted(bidirectional, 
                                                           key=lambda x: x[2]+x[3], 
                                                           reverse=True)[:5]:
                total = count_ab + count_ba
                print(f"  {city_a} ↔ {city_b}: {total:,} total ({count_ab:,} + {count_ba:,})")
    
    def export_html_report(self, output_file=None):
        """Export report as HTML file"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'city_mixing_report_{timestamp}.html'
        
        try:
            html_content = self._generate_html_content()
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ HTML report exported to: {output_file}")
        except Exception as e:
            print(f"❌ Error exporting HTML report: {e}")
    
    def _generate_html_content(self):
        """Generate HTML content for the report"""
        if not self.detection_data:
            return "<html><body><h1>No data available</h1></body></html>"
        
        stats = self.detection_data['stats']
        issues = self.detection_data['issues']
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>City Mixing Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #333; }}
                .stat {{ background: #f5f5f5; padding: 10px; margin: 10px 0; }}
                .issue {{ border-left: 4px solid #007cba; padding: 5px 15px; margin: 5px 0; }}
            </style>
        </head>
        <body>
            <h1>🏙️ City Mixing Analysis Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <div class="stat">
                <h2>📊 Summary</h2>
                <p>Total Kebabs: {stats['total_kebabs']:,}</p>
                <p>Mixing Issues: {stats['total_issues']:,}</p>
                <p>Affected Cities: {stats['affected_cities']:,}</p>
                <p>Issue Rate: {(stats['total_issues']/stats['total_kebabs']*100):.1f}%</p>
            </div>
        </body>
        </html>
        """
        
        return html

def main():
    parser = argparse.ArgumentParser(description='Generate city mixing reports')
    parser.add_argument('--detection-file', help='Detection results JSON file')
    parser.add_argument('--fix-file', help='Fix results JSON file')
    parser.add_argument('--city', help='Generate report for specific city')
    parser.add_argument('--patterns', action='store_true', help='Analyze mixing patterns')
    parser.add_argument('--html', action='store_true', help='Export as HTML')
    parser.add_argument('--output', help='Output file name')
    
    args = parser.parse_args()
    
    reporter = CityMixingReporter()
    
    # Auto-detect files if not specified
    detection_file = args.detection_file
    if not detection_file:
        detection_files = [f for f in os.listdir('.') 
                         if f.startswith('city_mixing_detection_') and f.endswith('.json')]
        if detection_files:
            detection_file = sorted(detection_files)[-1]
    
    if not reporter.load_data(detection_file, args.fix_file):
        return
    
    # Generate reports based on arguments
    if args.city:
        reporter.generate_city_report(args.city)
    elif args.patterns:
        reporter.generate_pattern_report()
    elif args.html:
        reporter.export_html_report(args.output)
    else:
        reporter.generate_summary_report()

if __name__ == '__main__':
    main()
