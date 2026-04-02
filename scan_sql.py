import re
import json

SQL_FILE = r'C:\Users\markowyy\Documents\kebsioronredesign\backups\supabase_dump_20260226_144452.sql'
OUTPUT_FILE = 'full_migration_data.json'

def parse_sql():
    data = {
        'cities': [],
        'kebab_places': [],
        'ratings': []
    }
    
    current_table = None
    
    with open(SQL_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if 'INSERT INTO "public"."cities"' in line:
                current_table = 'cities'
            elif 'INSERT INTO "public"."kebab_places"' in line:
                current_table = 'kebab_places'
            elif 'INSERT INTO "public"."ratings_history"' in line:
                current_table = 'ratings'
            
            if current_table and 'VALUES' in line:
                # Basic extraction of the values part
                values_part = line.split('VALUES', 1)[1].strip()
                # Remove trailing semicolon
                if values_part.endswith(';'):
                    values_part = values_part[:-1]
                
                # Split records - this is tricky because of commas inside strings
                # But for a quick scan, let's just see if we can find records
                data[current_table].append(values_part)
                
    print(f"Extracted segments: Cities: {len(data['cities'])}, Places: {len(data['kebab_places'])}, Ratings: {len(data['ratings'])}")
    
    # Just save the raw segments for now to see if we got them
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    parse_sql()
