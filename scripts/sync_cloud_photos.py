"""
SUPABASE CLOUD PHOTO SYNC v2.0
================================
Downloads kebab place photos from Google and stores them permanently
in Supabase Storage. Updates the DB with permanent CDN links.

Key fix in v2.0: Uses ID-cursor pagination to bypass the Supabase
client's hidden row limit (~500). Guarantees ALL records are reached.
"""
import os
import sys
import time
import unicodedata
import re
from dotenv import load_dotenv

# Add project root to path so we can import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.database import DatabaseService
from services.google_places import GooglePlacesService

def slugify(text):
    """Normalize text to ASCII for safe Supabase Storage keys."""
    if not text:
        return "unknown"
    replacements = {
        'ł': 'l', 'Ł': 'L', 'ó': 'o', 'Ó': 'O', 'ś': 's', 'Ś': 'S',
        'ą': 'a', 'Ą': 'A', 'ę': 'e', 'Ę': 'E', 'ń': 'n', 'Ń': 'N',
        'ź': 'z', 'Ź': 'Z', 'ż': 'z', 'Ż': 'Z', 'ć': 'c', 'Ć': 'C',
        'ö': 'o', 'ü': 'u', 'ä': 'a',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '_')
    return text


def fetch_all_needing_sync(db_service):
    """
    Fetch ALL kebab_places that need photo sync using ID-cursor pagination.
    This bypasses the Supabase client's hidden ~500 row cap.
    """
    all_records = []
    last_id = 0
    batch_size = 200  # Small batches are safest
    
    while True:
        response = db_service.client.table('kebab_places') \
            .select('id, name, photo_url, city_id') \
            .gt('id', last_id) \
            .order('id') \
            .limit(batch_size) \
            .execute()
        
        batch = response.data
        if not batch:
            break
        
        # Filter for records needing sync
        for p in batch:
            photo = p.get('photo_url')
            if photo and photo != 'NONE' and not photo.startswith('http') and len(photo) > 20:
                all_records.append(p)
        
        last_id = batch[-1]['id']
        
        # If we got fewer than batch_size, we've hit the end
        if len(batch) < batch_size:
            break
    
    return all_records


def sync_photos_to_cloud():
    load_dotenv()
    
    db_service = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    google_service = GooglePlacesService(os.getenv('GOOGLE_API_KEY'))
    bucket_name = 'kebab-photos'
    error_log_path = 'sync_errors.log'
    
    print("\n" + "="*60)
    print("🌩️  SUPABASE CLOUD PHOTO SYNC v2.0")
    print("="*60)
    
    # 1. Pre-fetch cities for fast lookup
    print("🏙️  Caching city names...")
    cities_res = db_service.client.table('cities').select('id, name').execute()
    city_map = {c['id']: c['name'] for c in cities_res.data}

    # 2. Fetch all places needing sync (ID-cursor pagination)
    print("📥 Fetching places needing sync (cursor pagination)...")
    to_sync = fetch_all_needing_sync(db_service)
    print(f"⚡ Places needing cloud sync: {len(to_sync)}")

    if not to_sync:
        print("\n✅ All photos are already in the cloud or marked as NONE.")
        return

    success_count = 0
    fail_count = 0
    skip_count = 0

    print(f"\n▶️ Starting sync... (errors logged to {error_log_path})\n")

    with open(error_log_path, 'a', encoding='utf-8') as err_log:
        err_log.write(f"\n--- SYNC v2.0 START: {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        
        for i, place in enumerate(to_sync):
            place_id = place['id']
            name = place['name']
            photo_ref = place['photo_url']
            city_id = place.get('city_id')
            city_name = city_map.get(city_id, 'Unknown')
            safe_city = slugify(city_name)
            storage_path = f"{safe_city}/{photo_ref}.jpg"

            try:
                # 1. Download from Google
                photo_response = google_service.gmaps.places_photo(
                    photo_reference=photo_ref,
                    max_width=800
                )
                
                image_data = b''
                for chunk in photo_response:
                    image_data += chunk
                
                if not image_data:
                    raise Exception("Google returned empty image data")

                # 2. Upload to Supabase Storage (skip if exists)
                try:
                    db_service.client.storage.from_(bucket_name).upload(
                        path=storage_path,
                        file=image_data,
                        file_options={"content-type": "image/jpeg"}
                    )
                except Exception as up_err:
                    if "already exists" not in str(up_err).lower() and "Duplicate" not in str(up_err):
                        raise up_err

                # 3. Get Public URL and update DB
                public_url = db_service.client.storage.from_(bucket_name).get_public_url(storage_path)
                
                db_service.client.table('kebab_places').update({
                    'photo_url': public_url,
                    'updated_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }).eq('id', place_id).execute()
                
                success_count += 1
                
            except Exception as e:
                err_msg = str(e)
                err_log.write(f"❌ ID={place_id} | {name} | {city_name} | {err_msg}\n")
                fail_count += 1

            # Progress every 10 items
            if (i + 1) % 10 == 0 or (i + 1) == len(to_sync):
                print(f"  [{i+1}/{len(to_sync)}] ✅ {success_count} synced | ❌ {fail_count} failed")
                
            time.sleep(0.05)

    print("\n" + "="*60)
    print(f"🏁 SYNC FINISHED")
    print(f"✅ Migrated: {success_count}")
    print(f"❌ Failed:   {fail_count}")
    if fail_count > 0:
        print(f"📝 See {error_log_path} for failure details.")
    print("="*60)


if __name__ == "__main__":
    sync_photos_to_cloud()
