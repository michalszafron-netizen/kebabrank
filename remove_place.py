"""
remove_place.py — Safely remove a kebab place and all its associated data from the database.

Usage:
  python remove_place.py "Yalla Kebab" --city Tychy
  python remove_place.py "Yalla Kebab" --city Tychy --confirm

Without --confirm it runs in DRY RUN mode (shows what would be deleted, no changes made).
Add --confirm to actually delete.
"""
import os
import sys
import io
import argparse
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

from services.pocketbase_db import PocketbaseService

def remove_place(place_name: str, city_name: str, confirm: bool = False):
    pb = PocketbaseService(os.getenv('PB_URL'))

    print(f"\n{'[DRY RUN] ' if not confirm else ''}Searching for: '{place_name}' in {city_name}...")

    # Find the city
    city_id = pb.get_city_id(city_name)
    if not city_id:
        print(f"  ERROR: City '{city_name}' not found in database.")
        return

    # Find kebab places in that city matching the name
    try:
        results = pb.client.collection('kebab_places').get_full_list(
            query_params={
                'filter': f'city="{city_id}" && name~"{place_name}"',
            }
        )
    except Exception as e:
        print(f"  ERROR searching kebab_places: {e}")
        return

    if not results:
        print(f"  No places found matching '{place_name}' in {city_name}.")
        return

    for place in results:
        print(f"\n  Found: [{place.id}] {place.name}")
        print(f"    Address: {getattr(place, 'address', 'N/A')}")
        print(f"    Google Place ID: {getattr(place, 'google_place_id', 'N/A')}")

        # Count associated records
        try:
            ratings = pb.client.collection('ratings').get_list(1, 1,
                query_params={'filter': f'kebab_place="{place.id}"'})
            ai_records = pb.client.collection('ai_analysis').get_list(1, 1,
                query_params={'filter': f'kebab_place="{place.id}"'})
            reviews = pb.client.collection('cached_reviews').get_list(1, 1,
                query_params={'filter': f'kebab_place="{place.id}"'})

            print(f"    Ratings records: {ratings.total_items}")
            print(f"    AI analysis records: {ai_records.total_items}")
            print(f"    Cached reviews: {reviews.total_items}")
        except Exception as e:
            if '404' not in str(e):
                print(f"    (Could not count associated records: {e})")

        if not confirm:
            print(f"\n  [DRY RUN] Would delete this place and all associated records.")
            print(f"  Run again with --confirm to execute the deletion.\n")
            continue

        # --- ACTUAL DELETION ---
        print(f"\n  Deleting associated records for [{place.id}] {place.name}...")

        # 1. Delete ratings
        try:
            all_ratings = pb.client.collection('ratings').get_full_list(
                query_params={'filter': f'kebab_place="{place.id}"'}
            )
            for r in all_ratings:
                pb.client.collection('ratings').delete(r.id)
            print(f"    Deleted {len(all_ratings)} rating(s)")
        except Exception as e:
            print(f"    Warning: Could not delete all ratings: {e}")

        # 2. Delete AI analysis
        try:
            all_ai = pb.client.collection('ai_analysis').get_full_list(
                query_params={'filter': f'kebab_place="{place.id}"'}
            )
            for r in all_ai:
                pb.client.collection('ai_analysis').delete(r.id)
            print(f"    Deleted {len(all_ai)} AI analysis record(s)")
        except Exception as e:
            print(f"    Warning: Could not delete AI analysis: {e}")

        # 3. Delete cached reviews
        try:
            all_reviews = pb.client.collection('cached_reviews').get_full_list(
                query_params={'filter': f'kebab_place="{place.id}"'}
            )
            for r in all_reviews:
                pb.client.collection('cached_reviews').delete(r.id)
            print(f"    Deleted {len(all_reviews)} cached review(s)")
        except Exception as e:
            if '404' not in str(e):
                print(f"    Warning: Could not delete cached reviews: {e}")

        # 4. Finally delete the kebab place itself
        try:
            pb.client.collection('kebab_places').delete(place.id)
            print(f"    ✅ Deleted place: {place.name} [{place.id}]")
        except Exception as e:
            print(f"    ERROR: Could not delete place: {e}")

    if not confirm:
        print("--- DRY RUN complete. No changes were made. ---")
    else:
        print("\n--- Removal complete. ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove a kebab place from the database.')
    parser.add_argument('name', help='Name (or partial name) of the kebab place to remove')
    parser.add_argument('--city', required=True, help='City where the place is located')
    parser.add_argument('--confirm', action='store_true',
                        help='Actually perform the deletion (default is dry run)')
    args = parser.parse_args()

    remove_place(args.name, args.city, confirm=args.confirm)
