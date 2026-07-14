"""Reset city rank history baseline."""
import os, io, sys, argparse
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def reset_history(cities=None, all_cities=False, dry_run=True):
    load_dotenv()
    pb = PocketbaseService(os.getenv("PB_URL"), os.getenv("PB_EMAIL"), os.getenv("PB_PASSWORD"))
    pb._ensure_auth()
    
    # 1. Get cities
    target_cities = []
    if all_cities:
        records = pb.client.collection('cities').get_full_list()
        target_cities = [(r.name, r.id) for r in records]
    elif cities:
        for name in cities:
            cid = pb.get_city_id(name)
            if cid: target_cities.append((name, cid))
    
    print(f"--- History Reset {'(DRY RUN)' if dry_run else ''} ---")
    
    for name, cid in target_cities:
        # Find all rating history except the most recent batch (today)
        # Strategy: Keep records created in the last 24 hours if they are the latest.
        # Simple strategy: Delete all rating history older than 6 hours for these cities.
        threshold = datetime.now(timezone.utc) - timedelta(hours=6)
        
        print(f"Processing {name} ({cid})...")
        
        # We need to fetch and delete
        page = 1
        to_delete = []
        while True:
            # Filter by city and older than threshold
            # Note: Pocketbase filter for dates uses "YYYY-MM-DD HH:MM:SS"
            ts = threshold.strftime("%Y-%m-%d %H:%M:%S")
            records = pb.client.collection('ratings').get_list(page, 200, {
                "filter": f'kebab_place.city="{cid}" && created < "{ts}"'
            })
            if not records.items: break
            to_delete.extend([r.id for r in records.items])
            if page * 200 >= records.total_items: break
            page += 1
            
        print(f"  Found {len(to_delete)} old records.")
        if not dry_run and to_delete:
            print(f"  Deleting {len(to_delete)} records...")
            for rid in to_delete:
                pb.client.collection('ratings').delete(rid)
            print(f"  ✅ Reset baseline for {name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--city', nargs='+')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    
    if not args.city and not args.all:
        print("Specify --city or --all")
        sys.exit(1)
        
    reset_history(cities=args.city, all_cities=args.all, dry_run=not args.execute)
