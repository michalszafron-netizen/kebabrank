import os

SQL_FILE = r'C:\Users\markowyy\Documents\kebsioronredesign\backups\supabase_dump_20260226_144452.sql'

def find_data():
    with open(SQL_FILE, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if 'public.cities' in line.lower() or 'public.kebab_places' in line.lower():
                print(f"L{i}: {line.strip()[:200]}")
            if i > 2000: # Scan more lines than before
                break

if __name__ == "__main__":
    find_data()
