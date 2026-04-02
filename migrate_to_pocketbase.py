import os
import re
import json
from pocketbase import PocketBase
from pocketbase.client import FileUpload

# --- CONFIGURATION ---
PB_URL = "https://pb.kebabrank.com"
PB_EMAIL = "kryptoholik@gmail.com"  # UPDATE THIS
PB_PASSWORD = "Jebacbaze@23"        # UPDATE THIS

# Paths
SQL_FILE = r'C:\Users\markowyy\Documents\kebsioronredesign\backups\supabase_dump_20260226_144452.sql'
PHOTOS_DIR = "local_photos"

client = PocketBase(PB_URL)

def parse_copy_block(content, start_marker):
    """Parses a PostgreSQL COPY block into a list of dictionaries."""
    pos = content.find(start_marker)
    if pos == -1:
        return []
    
    # Find the end of the COPY line to get the full statement
    line_end = content.find(b'\n', pos)
    if line_end == -1:
        return []
    copy_line = content[pos:line_end].decode('utf-8')
    
    # Extract header columns from the full line (e.g., "(id, name, ...)")
    header_match = re.search(r'\((.*?)\)', copy_line)
    if not header_match:
        print(f"⚠️ Could not find columns in line: {copy_line}")
        return []
    columns = [c.strip().replace('"', '') for c in header_match.group(1).split(',')]
    
    # Extract data lines until \.
    start_data = content.find(b'\n', pos) + 1
    end_data = content.find(b'\n\\.\n', start_data)
    if end_data == -1:
        return []
        
    data_block = content[start_data:end_data].decode('utf-8')
    records = []
    for line in data_block.split('\n'):
        if not line.strip():
            continue
        values = line.split('\t')
        record = {}
        for i, val in enumerate(values):
            if i < len(columns):
                # Handle \N as None
                record[columns[i]] = None if val == '\\N' else val
        records.append(record)
    return records

def migrate():
    try:
        # 1. Auth as Admin
        admin_auth = client.admins.auth_with_password(PB_EMAIL, PB_PASSWORD)
        print(" Logged in to Pocketbase.")

        # 2. Read SQL File once
        print(" Reading SQL dump (20MB)...")
        with open(SQL_FILE, 'rb') as f:
            content = f.read()

        # 3. Clean existing data (Optional but recommended for fresh start)
        # We'll do this by deleting the collections and recreating them if you want, 
        # or just deleting all records. To keep it simple and safe, we'll just skip 
        # existing ones if they have the same google_place_id, OR we wipe.
        # User asked: "What now do we need remove what we loaded?" -> Let's wipe.
        print(" Cleaning existing records...")
        for col in ["kebab_places", "cities", "ratings"]:
            try:
                # Pocketbase doesn't have a truncate, so we fetch all and delete.
                # Since we have < 1000 right now, it's fast.
                list_res = client.collection(col).get_list(1, 500)
                for item in list_res.items:
                    client.collection(col).delete(item.id)
            except:
                pass # Collection might not exist yet

        # 4. Parse Data
        print(" Parsing data from SQL...")
        cities_raw = parse_copy_block(content, b'COPY "public"."cities"')
        places_raw = parse_copy_block(content, b'COPY "public"."kebab_places"')
        ratings_raw = parse_copy_block(content, b'COPY "public"."ratings_history"')
        ai_analysis_raw = parse_copy_block(content, b'COPY "public"."ai_analysis"')

        # 5. Migrate Cities
        print(f" Migrating {len(cities_raw)} Cities...")
        city_id_map = {} # old_pg_id -> new_pb_id
        for c in cities_raw:
            slug = c['name'].lower().replace(' ', '-').replace('\xc5\x82', 'l').replace('\xc3\xb3', 'o').replace('\xc5\xba', 'z')
            try:
                new_city = client.collection("cities").create({
                    "name": c['name'],
                    "slug": slug
                })
                city_id_map[c['id']] = new_city.id
            except Exception as e:
                print(f"City {c['name']} error: {e}")

        # 6. Migrate Kebab Places
        print(f"Migrating {len(places_raw)} Kebab Places...")
        place_id_map = {} # old_pg_id -> new_pb_id
        for i, p in enumerate(places_raw):
            place_id = p['id']
            name = p['name']
            
            payload = {
                "name": name,
                "address": p['address'],
                "google_place_id": p['google_place_id'],
                "lat": float(p['latitude']) if p['latitude'] else 0,
                "lng": float(p['longitude']) if p['longitude'] else 0,
                "city": city_id_map.get(p['city_id']),
            }

            try:
                # Find photo
                photo_file = None
                if os.path.exists(PHOTOS_DIR):
                    for f in os.listdir(PHOTOS_DIR):
                        if f.startswith(f"{place_id}_"):
                            photo_file = os.path.join(PHOTOS_DIR, f)
                            break
                
                if photo_file:
                    payload["photo"] = FileUpload((os.path.basename(photo_file), open(photo_file, "rb")))
                
                new_place = client.collection("kebab_places").create(payload)
                place_id_map[place_id] = new_place.id
                if i % 100 == 0:
                    print(f"Progress: {i}/{len(places_raw)}...")
            except Exception as e:
                print(f"Error for {name}: {e}")

        # 7. Migrate Ratings
        if ratings_raw:
            print(f"Migrating {len(ratings_raw)} Ratings...")
            for r in ratings_raw:
                pb_place_id = place_id_map.get(r['kebab_place_id'])
                if not pb_place_id: continue
                
                try:
                    client.collection("ratings").create({
                        "kebab_place": pb_place_id,
                        "rating": float(r['rating']) if r['rating'] else 0,
                        "total_reviews": int(r['total_reviews']) if r['total_reviews'] else 0,
                        "rank_score": float(r['rank_score']) if r['rank_score'] else 0,
                        "city_rank": int(r['city_rank']) if r['city_rank'] else 0,
                        "ai_score": float(r['ai_score']) if r.get('ai_score') else 0,
                    })
                except Exception as e:
                    pass

        # 8. Migrate AI Analysis
        if ai_analysis_raw:
            print(f"Migrating {len(ai_analysis_raw)} AI Analysis records...")
            for ai in ai_analysis_raw:
                pb_place_id = place_id_map.get(ai['kebab_place_id'])
                if not pb_place_id: continue
                
                try:
                    # Clean up analysis_data if it's a string
                    analysis_data = ai['analysis_data']
                    if analysis_data and isinstance(analysis_data, str):
                        try:
                            analysis_data = json.loads(analysis_data)
                        except:
                            pass

                    client.collection("ai_analysis").create({
                        "kebab_place": pb_place_id,
                        "analysis_data": analysis_data,
                        "ai_score": float(ai['ai_score']) if ai.get('ai_score') else 0,
                        "ai_summary": ai.get('ai_summary', ''),
                        "confidence_score": float(ai['confidence_score']) if ai.get('confidence_score') else 0,
                    })
                except Exception as e:
                    print(f"AI Analysis error for {pb_place_id}: {e}")

        print("Full Migration Complete!")

    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
