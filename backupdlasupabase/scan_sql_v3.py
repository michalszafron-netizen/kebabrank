import os

SQL_FILE = r'C:\Users\markowyy\Documents\kebsioronredesign\backups\supabase_dump_20260226_144452.sql'

def find_data():
    with open(SQL_FILE, 'rb') as f:
        content = f.read()
        
    print(f"File size: {len(content)} bytes")
    
    patterns = [b'INSERT INTO', b'COPY', b'cities', b'kebab_places']
    for p in patterns:
        pos = content.find(p)
        if pos != -1:
            # Show a bit of context around the first match
            context = content[max(0, pos-50):pos+150]
            print(f"Match for {p} at {pos}: {context}")
        else:
            print(f"No match for {p}")

if __name__ == "__main__":
    find_data()
