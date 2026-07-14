import os
import sys
import io
import argparse
from typing import List, Dict
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService
from services.gmaps_extractor import GmapsextractorService
import time

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def update_missing_photos(city_name: str = None, dry_run: bool = False, limit: int = None):
    load_dotenv()
    
    # Initialize services
    pb = PocketbaseService(os.getenv('PB_URL'))
    pb._ensure_auth()
    
    gmaps_key = os.getenv('GMAPS_EXTRACTOR_API_KEY') or "ZUaHNRMieiVzFcAOvmyZ6tMjK9U4HDLN4MVejoLgmyn0K7LB"
    gmaps = GmapsextractorService(gmaps_key)
    
    print("\n" + "="*60)
    print("📸 KEBAB PHOTO UPDATER (Standalone)")
    print("="*60)
    
    # 1. Fetch places missing photos
    filter_query = 'photo = ""'
    if city_name:
        city_id = pb.get_city_id(city_name)
        if not city_id:
            print(f"Error: City {city_name} not found.")
            return
        filter_query += f' && city = "{city_id}"'
        
    try:
        places = pb.client.collection('kebab_places').get_full_list(query_params={
            "filter": filter_query
        })
    except Exception as e:
        print(f"Error fetching places: {e}")
        return
        
    if not places:
        print(f"✅ No places missing photos found for {city_name if city_name else 'all cities'}.")
        return
        
    print(f"🔍 Found {len(places)} places missing photos.")
    if limit:
        places = places[:limit]
        print(f"   (Limiting to {limit} places based on --limit)")
        
    success_count = 0
    fail_count = 0
    
    for i, p in enumerate(places):
        print(f"[{i+1}/{len(places)}] '{p.name}' ({p.address})...")
        
        if dry_run:
            print("  [DRY RUN] Would search and update photo.")
            success_count += 1
            continue
            
        # 2. Search for the place to get Featured Image
        # Using name + city/address for accuracy
        query = f"kebab {p.name} {p.address}"
        
        results = []
        max_retries = 2
        for attempt in range(max_retries + 1):
            results = gmaps.search_places(query, page=1)
            if results or attempt == max_retries:
                break
            print(f"  ⏳ Retrying search... ({attempt + 1}/{max_retries})")
            time.sleep(2)
            
        if not results:
            # Try a broader search if exact address failed
            query = f"kebab {p.name} {city_name if city_name else ''}"
            for attempt in range(max_retries + 1):
                results = gmaps.search_places(query, page=1)
                if results or attempt == max_retries:
                    break
                print(f"  ⏳ Retrying broad search... ({attempt + 1}/{max_retries})")
                time.sleep(2)
            
        photo_found = False
        if results:
            # Matching logic: find the one with same ID or best name match
            best_match = None
            for item in results:
                if item.get('Place Id') == p.google_place_id:
                    best_match = item
                    break
            
            # Fallback to first result if ID didn't match but it's clearly a small search
            if not best_match and len(results) > 0:
                best_match = results[0]
                
            if best_match:
                photo_url = best_match.get('Featured Image')
                if photo_url:
                    print(f"  ✨ Found image: {photo_url[:50]}...")
                    if pb.upload_place_photo(p.id, photo_url):
                        print("  ✅ Photo uploaded successfully.")
                        photo_found = True
                        success_count += 1
                    else:
                        print("  ❌ Upload failed.")
                else:
                    print("  ℹ️ No 'Featured Image' in API response.")
            else:
                print("  ⚠️ Could not find a reliable match in search results.")
        else:
            print("  ⚠️ No search results found.")
            
        if not photo_found:
            fail_count += 1
            
        # Tiny delay to avoid rate limiting
        time.sleep(0.5)

    print("\n" + "="*60)
    print(f"🏁 FINISHED")
    print(f"✨ Photos updated: {success_count}")
    print(f"❌ Failed/Skipped: {fail_count}")
    print("="*60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--city', help='Filter by city name')
    parser.add_argument('--limit', type=int, help='Limit number of places to process')
    parser.add_argument('--dry-run', action='store_true', help='Don\'t perform actual updates')
    args = parser.parse_args()
    
    update_missing_photos(args.city, args.dry_run, args.limit)
