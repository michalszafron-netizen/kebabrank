import os

SQL_FILE = r'C:\Users\markowyy\Documents\kebsioronredesign\backups\supabase_dump_20260226_144452.sql'

def find_data():
    with open(SQL_FILE, 'rb') as f:
        content = f.read()
    
    targets = [b'COPY "public"."cities"', b'COPY "public"."kebab_places"', b'COPY "public"."ratings_history"']
    for t in targets:
        pos = content.find(t)
        if pos != -1:
            print(f"Match for {t} at {pos}")
            # Show a bit of the data after the COPY line
            context = content[pos:pos+500]
            print(f"Data snippet: {context}\n")
        else:
            print(f"No match for {t}")

if __name__ == "__main__":
    find_data()
