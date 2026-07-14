# update_place_photos.py - Script to fetch and update real photos for kebab places
import os
import time
from dotenv import load_dotenv
from services.database import DatabaseService
from services.google_places import GooglePlacesService

def update_photos():
    load_dotenv()
    
    # Initialize services
    db_service = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    google_service = GooglePlacesService(os.getenv('GOOGLE_API_KEY'))
    
    print("\n" + "="*60)
    print("🚀 KEBAB PHOTO UPDATER v3.0 (Smart Sync)")
    print("="*60)
    
    # 1. Fetch ALL places to see current status
    try:
        print("📥 Fetching database records...")
        all_places = []
        page = 0
        page_size = 1000
        while True:
            response = db_service.client.table('kebab_places') \
                .select('id, name, google_place_id, photo_url') \
                .range(page * page_size, (page + 1) * page_size - 1) \
                .execute()
            if not response.data: break
            all_places.extend(response.data)
            if len(response.data) < page_size: break
            page += 1
            
        total_in_db = len(all_places)
        print(f"📊 Total places in database: {total_in_db}")
        
        # Filter for places that actually need an update
        # We skip if photo_url is already a valid-looking reference (longer than 10 chars)
        # We also skip if it's 'NONE' (already checked and not found)
        places_to_update = [
            p for p in all_places 
            if not p.get('photo_url') or (len(p.get('photo_url')) < 10 and p.get('photo_url') != 'NONE')
        ]
        
        already_done = total_in_db - len(places_to_update)
        print(f"📈 Progress: {already_done}/{total_in_db} places already have data.")
        print(f"⚡ {len(places_to_update)} places left to process.")
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return

    if not places_to_update:
        print("\n✅ WORK COMPLETE! All kebab places have photo data or were verified.")
        return

    updated_count = 0
    skipped_count = 0
    error_count = 0

    print("\n▶️ Starting fetching process...\n")

    for i, place in enumerate(places_to_update):
        place_id = place['id']
        name = place['name']
        google_id = place['google_place_id']

        print(f"[{i+1}/{len(places_to_update)}] '{name}'...")

        if not google_id:
            print(f"  ⚠️ Skipping - Missing Google ID")
            skipped_count += 1
            continue

        try:
            # Fetch photo reference from Google
            details = google_service.gmaps.place(
                place_id=google_id,
                fields=['photo'],
                language='pl'
            )
            
            result = details.get('result', {})
            photos = result.get('photos', [])
            
            if not photos:
                # Mark as NONE so we don't pay to check it again
                db_service.client.table('kebab_places').update({
                    'photo_url': 'NONE',
                    'updated_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }).eq('id', place_id).execute()
                print(f"  ℹ️ No photos found. Marked as NONE (saved status).")
                skipped_count += 1
                continue
                
            photo_ref = photos[0].get('photo_reference')
            
            # Update the database
            db_service.client.table('kebab_places').update({
                'photo_url': photo_ref,
                'updated_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }).eq('id', place_id).execute()
            
            print(f"  ✨ Success! Photo Ref: {photo_ref[:30]}...")
            updated_count += 1
            
            # Small delay to keep Google happy
            time.sleep(0.05) 
            
        except Exception as e:
            msg = str(e)
            if "NOT_FOUND" in msg:
                print(f"  ❌ Google ID obsolete (No longer in Maps).")
            else:
                print(f"  ❌ Error: {msg}")
            error_count += 1

    print("\n" + "="*60)
    print(f"🏁 BATCH FINISHED")
    print(f"✨ New photos added: {updated_count}")
    print(f"⏭️  Verified (No photos): {skipped_count}")
    print(f"❌ Errors/Obsolete: {error_count}")
    print("="*60)
    print("Tips: If you see many errors, Google might have updated their IDs.")

if __name__ == "__main__":
    update_photos()
