import os
import sys
import io
import argparse
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def cleanup_mismatches(city_name: str, dry_run: bool = False):
    load_dotenv()
    pb = PocketbaseService(os.getenv('PB_URL'))
    pb._ensure_auth()
    
    city_id = pb.get_city_id(city_name)
    if not city_id:
        print(f"City {city_name} not found.")
        return

    print(f"--- Cleaning up city mismatches for {city_name} ---")
    
    # Get all places currently assigned to this city
    records = pb.client.collection('kebab_places').get_full_list(query_params={
        "filter": f'city="{city_id}"'
    })
    
    print(f"Checking {len(records)} places...")
    
    deleted_count = 0
    kept_count = 0
    
    city_lower = city_name.lower()
    
    for r in records:
        address = getattr(r, 'address', '').lower()
        name = getattr(r, 'name', '').lower()
        
        # Check if city name is in address
        # We also check the name just in case the location is "Kebab Tychy" but address is weird
        if city_lower in address or city_lower in name:
            kept_count += 1
            continue
            
        # If we are here, it's likely a mismatch
        print(f"MISMATCH FOUND: {r.name} | Address: {r.address}")
        
        if not dry_run:
            try:
                # 1. Delete associated ratings history first (to avoid orphan records if possible, 
                # though PB usually handles this if relations are set to cascade. 
                # For safety, we just delete the place)
                pb.client.collection('kebab_places').delete(r.id)
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {r.name}: {e}")
        else:
            deleted_count += 1

    print("-" * 30)
    if dry_run:
        print(f"[DRY RUN] Would have deleted {deleted_count} places. Kept {kept_count}.")
    else:
        print(f"✓ Deleted {deleted_count} misattributed places. Kept {kept_count}.")
    print("-" * 30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('city', help='City name to clean up')
    parser.add_argument('--dry-run', action='store_true', help='Report findings without deleting')
    args = parser.parse_args()
    
    cleanup_mismatches(args.city, args.dry_run)
