"""
Cleanup Non-Kebab Places from Database
======================================
Scans all kebab_places in PocketBase and removes places that are clearly
NOT kebab restaurants (e.g., sushi, Indian, Chinese, steakhouse, etc.).

Usage:
    python cleanup_non_kebab.py              # Dry run (default)
    python cleanup_non_kebab.py --execute    # Actually delete records
    python cleanup_non_kebab.py --city Zakopane  # Only check one city
"""
import os
import sys
import io
import argparse
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Keywords that STRONGLY indicate it IS a kebab place
KEBAB_WHITELIST = [
    'kebab', 'kebap', 'kebaya', 'keb', 'ke-bab', 'kabab',
    'doner', 'döner', 'dürüm', 'durum',
    'shawarma', 'szawarma', 'shorma', 'shawerma', 'shaurma',
    'gyros', 'gyro', 'pita', 'wrap',
    'falafel', 'turkish', 'turecki', 'turecka', 'istanbul',
    'ali baba', 'sultan', 'efes', 'ankara', 'antalya',
    'lahmacun', 'adana', 'iskender', 'tantuni', 'street food',
    'piri-piri', 'piri piri', 'sapko', 'u pajdy', 'kura warzyw',
    'kapsalon', 'petarda', 'krafciak', 'gastrofaza', 'taksim',
    'kraft', 'alibaba', 'złota kura',
]

# Keywords that indicate NOT a kebab place (only if NO whitelist match)
NOT_KEBAB_BLACKLIST = [
    'sushi', 'ramen', 'pho', 'wok', 'china', 'chiński', 'chinski',
    'indian', 'indyjska', 'indyjski', 'india', 'curry house', 'tandoori',
    'steak', 'steakhouse',
    'ice cream', 'lody', 'lodziarnia', 'cukiernia', 'bakery', 'piekarnia',
    'hotel', 'hostel', 'motel',
    'apteka', 'pharmacy',
    'thai', 'tajska', 'vietnamese', 'wietnamska',
    'japanese', 'japońska', 'japonska',
    'mexican', 'meksykańska', 'meksykanska',
]


def is_not_kebab(name: str) -> bool:
    """
    Strict filter: Returns True if the place should be REMOVED.
    
    Logic (strict — matches update_city_gmaps.py):
    - If name contains a kebab whitelist keyword → KEEP (return False)
    - If name contains a blacklist keyword → REMOVE (return True)
    - If name has NO kebab keyword at all → REMOVE (return True)
    
    Since cleanup only has names (no Google Maps categories), 
    any place without a kebab keyword in its name is suspicious.
    """
    name_lower = name.lower()
    # If name contains a kebab keyword, it's definitely fine
    if any(kw in name_lower for kw in KEBAB_WHITELIST):
        return False
    # No kebab keyword found → flag for removal
    return True


def cleanup(execute: bool = False, cities: list = None, scan_all: bool = False):
    load_dotenv()
    pb = PocketbaseService(os.getenv("PB_URL"), os.getenv("PB_EMAIL"), os.getenv("PB_PASSWORD"))
    pb._ensure_auth()

    print("=" * 60)
    print("🧹 NON-KEBAB PLACE CLEANUP")
    print(f"   Mode: {'🔴 EXECUTE (will delete)' if execute else '🟢 DRY RUN (preview only)'}")
    if cities:
        print(f"   Cities: {', '.join(cities)}")
    elif scan_all:
        print(f"   Scope: ALL cities")
    print("=" * 60)

    # Resolve city IDs if filtering by city
    city_ids = []
    if cities:
        for city_name in cities:
            cid = pb.get_city_id(city_name)
            if not cid:
                print(f"  ⚠️ City '{city_name}' not found in DB, skipping.")
            else:
                city_ids.append((city_name, cid))
        if not city_ids:
            print("Error: No valid cities found.")
            return

    flagged = []
    page = 1
    total_scanned = 0

    while True:
        try:
            query_params = {}
            if city_ids:
                # Build filter for multiple cities: city="id1" || city="id2" ...
                city_filter_parts = [f'city="{cid}"' for _, cid in city_ids]
                query_params["filter"] = " || ".join(city_filter_parts)

            results = pb.client.collection('kebab_places').get_list(page, 200, query_params)
            if not results.items:
                break

            for item in results.items:
                total_scanned += 1
                if is_not_kebab(item.name):
                    flagged.append({
                        'id': item.id,
                        'name': item.name,
                        'address': getattr(item, 'address', ''),
                    })

            if page * 200 >= results.total_items:
                break
            page += 1
        except Exception as e:
            print(f"Error scanning page {page}: {e}")
            break

    print(f"\nScanned {total_scanned} places.")
    print(f"Found {len(flagged)} non-kebab places:\n")

    for i, place in enumerate(flagged, 1):
        print(f"  [{i}] {place['name']}")
        print(f"      Address: {place['address']}")
        print(f"      ID: {place['id']}")

    if not flagged:
        print("  ✅ No non-kebab places found. Database is clean!")
        return

    if not execute:
        print(f"\n🟢 DRY RUN - No changes made.")
        print(f"   Run with --execute to delete these {len(flagged)} records.")
        return

    # Execute deletion
    print(f"\n🔴 DELETING {len(flagged)} non-kebab places...")
    deleted = 0
    for place in flagged:
        try:
            # First delete any ratings for this place
            try:
                ratings = pb.client.collection('ratings').get_list(1, 200, {
                    "filter": f'kebab_place="{place["id"]}"'
                })
                for r in ratings.items:
                    pb.client.collection('ratings').delete(r.id)
            except:
                pass

            # Then delete any AI analysis
            try:
                ai = pb.client.collection('ai_analysis').get_list(1, 10, {
                    "filter": f'kebab_place="{place["id"]}"'
                })
                for a in ai.items:
                    pb.client.collection('ai_analysis').delete(a.id)
            except:
                pass

            # Finally delete the place itself
            pb.client.collection('kebab_places').delete(place['id'])
            deleted += 1
            print(f"  ✅ Deleted: {place['name']}")
        except Exception as e:
            print(f"  ❌ Error deleting {place['name']}: {e}")

    print(f"\n🏁 DONE — Deleted {deleted}/{len(flagged)} non-kebab records.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remove non-kebab places from database",
        epilog="Examples:\n"
               "  python cleanup_non_kebab.py --city Tychy Zakopane\n"
               "  python cleanup_non_kebab.py --city Tychy --execute\n"
               "  python cleanup_non_kebab.py --all\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--execute", action="store_true", help="Actually delete (default is dry-run)")
    parser.add_argument("--city", nargs="+", type=str, default=None, help="One or more city names to check")
    parser.add_argument("--all", action="store_true", dest="scan_all", help="Scan ALL cities in the database")
    args = parser.parse_args()

    if not args.city and not args.scan_all:
        print("⚠️ Please specify --city <name(s)> or --all")
        print("   Example: python cleanup_non_kebab.py --city Tychy Zakopane")
        print("   Example: python cleanup_non_kebab.py --all")
        sys.exit(1)

    cleanup(execute=args.execute, cities=args.city, scan_all=args.scan_all)

