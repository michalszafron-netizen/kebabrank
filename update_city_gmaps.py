import os
import sys
import io
import json
import re
from dotenv import load_dotenv
from services.dataforseo import DataForSEOService
from services.pocketbase_db import PocketbaseService
from services.ranking import RankingService
from datetime import datetime

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── Kebab Qualification Filter ──────────────────────────────────────────
KEBAB_NAME_WHITELIST = [
    'kebab', 'kebap', 'kebaya', 'keb', 'ke-bab', 'kabab',
    'doner', 'döner', 'dürüm', 'durum',
    'shawarma', 'szawarma', 'shorma', 'shawerma', 'shaurma',
    'gyros', 'gyro ', 'pita', 'wrap',
    'falafel', 'turkish', 'turecki', 'turecka', 'istanbul',
    'ali baba', 'sultan', 'efes', 'ankara', 'antalya',
    'lahmacun', 'adana', 'iskender', 'tantuni', 'street food',
    'piri-piri', 'piri piri', 'sapko', 'u pajdy', 'kura warzyw',
    'kapsalon', 'petarda', 'krafciak', 'gastrofaza', 'taksim',
    'kraft', 'alibaba', 'złota kura',
]

KEBAB_NAME_BLACKLIST = [
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

# DataForSEO category_ids that confirm a kebab place
KEBAB_CAT_IDS = [
    'kebab_shop', 'doner_kebab_restaurant', 'shawarma_restaurant',
    'gyros_restaurant', 'falafel_restaurant', 'middle_eastern_restaurant',
]

# DataForSEO category names (category + additional_categories fields)
KEBAB_CATEGORY_WHITELIST = [
    'kebab', 'doner', 'döner', 'turkish', 'middle eastern',
    'fast food', 'shawarma', 'gyro', 'falafel', 'pita',
    'take out', 'takeaway', 'meal takeaway',
]

KEBAB_CATEGORY_BLACKLIST = [
    'sushi', 'indian', 'chinese', 'japanese', 'thai', 'vietnamese',
    'steakhouse', 'ice cream', 'bakery', 'hotel', 'bar',
    'italian restaurant', 'french restaurant', 'spanish restaurant',
]

# Cities large enough to exceed 100 results in Google Maps kebab search
LARGE_CITIES = {
    'krakow', 'kraków',
    'warszawa', 'warsaw',
    'katowice',
    'poznan', 'poznań',
    'wroclaw', 'wrocław',
    'gdansk', 'gdańsk',
    'gdynia',
    'lodz', 'łódź',
}

def normalize_polish(s: str) -> str:
    return s.lower().translate(str.maketrans('ąćęłńóśźż', 'acelnoszz'))


def parse_opening_hours(work_hours: dict) -> dict:
    """
    Convert DataForSEO work_hours.timetable to our JSON format.
    Input: {"timetable": {"monday": [{"open": {"hour": 10, "minute": 30}, "close": {...}}], ...}}
    Output: {"1": "10:30-22:30", "0": "11:00-22:30", ...}  (0=Sun, 1=Mon, ..., 6=Sat)

    Edge cases:
    - No timetable but current_status="open"  → {"_status": "open"}   (show Otwarte badge)
    - No timetable but current_status="closed" → {"_status": "closed"} (show Zamknięte badge)
    """
    if not work_hours:
        return {}
    timetable = work_hours.get('timetable') or {}

    if not timetable:
        status = work_hours.get('current_status', '')
        if status in ('open', 'closed', 'temporarily_closed', 'permanently_closed'):
            return {'_status': 'closed' if 'closed' in status else 'open'}
        return {}
    day_map = {
        'sunday': '0', 'monday': '1', 'tuesday': '2',
        'wednesday': '3', 'thursday': '4', 'friday': '5', 'saturday': '6',
    }
    result = {}
    for day_name, slots in timetable.items():
        day_num = day_map.get(day_name.lower())
        if not day_num:
            continue
        if not slots:
            result[day_num] = None
            continue
        slot = slots[0]
        o = slot.get('open') or {}
        c = slot.get('close') or {}
        if o and c and 'hour' in o and 'hour' in c:
            result[day_num] = (
                f"{o['hour']:02d}:{o.get('minute', 0):02d}"
                f"-{c['hour']:02d}:{c.get('minute', 0):02d}"
            )
        else:
            result[day_num] = None
    return result


def is_kebab_place(item: dict) -> bool:
    """
    Strict kebab qualification filter for DataForSEO SERP Maps items.
    Returns True ONLY if there is positive evidence the place serves kebab.
    """
    name = (item.get('title') or '').lower()
    cats = [item.get('category', '')] + (item.get('additional_categories') or [])
    cat_ids = item.get('category_ids') or []
    categories_lower = ' '.join(c.lower() for c in cats if c)
    cat_ids_str = ' '.join(c.lower() for c in cat_ids)

    # category_ids are most reliable (standardized Google taxonomy)
    if any(kw in cat_ids_str for kw in KEBAB_CAT_IDS):
        return True

    # Name whitelist → always include
    if any(kw in name for kw in KEBAB_NAME_WHITELIST):
        return True

    # Name blacklist (no whitelist match) → exclude
    if any(kw in name for kw in KEBAB_NAME_BLACKLIST):
        return False

    # Category name whitelist → include
    if any(kw in categories_lower for kw in KEBAB_CATEGORY_WHITELIST):
        return True

    # No evidence → exclude
    return False


def update_city(city_name: str, login: str, password: str):
    load_dotenv()

    dfs = DataForSEOService(login, password)
    pb = PocketbaseService(os.getenv('PB_URL'))
    ranker = RankingService()

    print(f"--- Updating {city_name} via DataForSEO ---")

    city_id = pb.get_city_id(city_name)
    if not city_id:
        print(f"Error: City '{city_name}' not found in database.")
        return

    pb.reset_city_ranks(city_id)

    # 1. Search for kebabs in city
    is_large = normalize_polish(city_name) in LARGE_CITIES
    depth = 400 if is_large else 100
    print(f"Searching DataForSEO for: 'kebab {city_name}' (depth={depth})...")
    all_results = dfs.search_places(f"kebab {city_name}", depth=depth)

    if not all_results:
        print("No results from DataForSEO.")
        return

    # For large cities: if we still hit the cap, supplement with alternative keywords
    if len(all_results) >= depth:
        found_ids = {item.get('place_id') for item in all_results}
        for extra_kw in [f"döner {city_name}", f"shawarma {city_name}"]:
            print(f"  Hit cap ({depth}), supplementing with: '{extra_kw}'...")
            extra = dfs.search_places(extra_kw, depth=100)
            added = 0
            for item in extra:
                if item.get('place_id') and item.get('place_id') not in found_ids:
                    all_results.append(item)
                    found_ids.add(item['place_id'])
                    added += 1
            print(f"  Added {added} new places from '{extra_kw}'")
            if added == 0:
                break  # no new results, stop trying

    found_google_ids = {item.get('place_id') for item in all_results if item.get('place_id')}

    # 2. Cross-check top-10 existing places (catch any missed by search)
    existing_places = pb.client.collection('kebab_places').get_full_list(
        query_params={"filter": f'city="{city_id}"'}
    )
    existing_ids_before = {
        getattr(p, 'google_place_id', '') for p in existing_places
        if getattr(p, 'google_place_id', '')
    }

    report_closed_temp = []
    report_closed_perm = []
    report_new = []

    top_existing = sorted(
        existing_places,
        key=lambda p: getattr(p, 'city_rank', 999) or 999
    )[:10]

    missed_count = 0
    for ep in top_existing:
        g_id = getattr(ep, 'google_place_id', '')
        if g_id and g_id not in found_google_ids:
            print(f"  Explicitly fetching missing top place: {ep.name}")
            try:
                explicit = dfs.search_places(f"{ep.name} {city_name}")
                for raw in explicit:
                    if raw.get('place_id') == g_id:
                        all_results.append(raw)
                        found_google_ids.add(g_id)
                        missed_count += 1
                        print(f"    ✓ Found and recovered: {ep.name}")
                        break
            except Exception as e:
                print(f"    Failed to fetch {ep.name}: {e}")

    print(f"Found {len(all_results)} places total ({missed_count} recovered). Processing...")

    # 3. Filter and prepare data
    places_to_save = []
    skipped_non_kebab = 0
    seen_ids = set()

    for item in all_results:
        g_id = item.get('place_id')
        if not g_id or g_id in seen_ids:
            continue
        seen_ids.add(g_id)

        # City filter using address_info (DataForSEO gives parsed city directly)
        address_info = item.get('address_info') or {}
        item_city = (address_info.get('city') or '').strip()

        if item_city:
            if normalize_polish(city_name) not in normalize_polish(item_city) and \
               normalize_polish(item_city) not in normalize_polish(city_name):
                print(f"  ⛔ Skipping {item.get('title')} - Not in {city_name} (city: {item_city})")
                continue
        else:
            # Fallback: postal code check in full address string
            full_address = item.get('address') or ''
            parts = [p.strip() for p in full_address.split(',')]
            city_chunk = None
            for part in parts:
                if re.search(r'\b\d{2}-\d{3}\b', part):
                    city_chunk = part
                    break
            if city_chunk is None:
                print(f"  ⛔ Skipping {item.get('title')} - No Polish postal code ({full_address})")
                continue
            if normalize_polish(city_name) not in normalize_polish(city_chunk):
                print(f"  ⛔ Skipping {item.get('title')} - Not in {city_name} (chunk: {city_chunk})")
                continue

        # Kebab qualification
        if not is_kebab_place(item):
            cats = [item.get('category', '')] + (item.get('additional_categories') or [])
            print(f"  🚫 Skipping {item.get('title')} - Not a kebab place (cats: {cats})")
            skipped_non_kebab += 1
            continue

        # Parse opening hours from DataForSEO work_hours
        opening_hours = parse_opening_hours(item.get('work_hours'))

        rating_obj = item.get('rating') or {}
        place_data = {
            'name': item.get('title'),
            'address': item.get('address', ''),
            'google_place_id': g_id,
            'rating': float(rating_obj.get('value') or 0),
            'total_reviews': int(rating_obj.get('votes_count') or 0),
            'lat': float(item.get('latitude') or 0),
            'lng': float(item.get('longitude') or 0),
            'opening_hours': json.dumps(opening_hours, ensure_ascii=False) if opening_hours else None,
            'photo': item.get('main_image'),
        }
        places_to_save.append(place_data)

    if skipped_non_kebab > 0:
        print(f"  ℹ️ Filtered out {skipped_non_kebab} non-kebab places.")

    # 3b. Closed status check for places with no opening hours (null timetable in SERP)
    # — Temporarily/permanently closed places typically have no timetable in Google Maps.
    # — Batch-check these via my_business_info to get definitive status.
    suspects = [
        p for p in places_to_save
        if not p.get('opening_hours')  # null timetable from SERP → might be closed
    ]
    if suspects:
        print(f"\n  Checking closed status for {len(suspects)} place(s) with no hours...")
        check_list = [
            {'google_place_id': p['google_place_id'], 'name': p['name'], 'city': city_name}
            for p in suspects
        ]
        status_map = dfs.check_businesses_status(check_list)
        confirmed_open = []
        for p in places_to_save:
            status = status_map.get(p['google_place_id'])
            if status == 'temporarily_closed':
                report_closed_temp.append({'name': p['name'], 'google_place_id': p['google_place_id']})
                print(f"  ⏸️  Removing {p['name']} - Temporarily closed")
            elif status == 'permanently_closed':
                report_closed_perm.append({'name': p['name'], 'google_place_id': p['google_place_id']})
                print(f"  🔒 Removing {p['name']} - Permanently closed")
            else:
                confirmed_open.append(p)
        places_to_save = confirmed_open

    # 4. Rank
    ranked_kebabs = ranker.rank_kebabs(places_to_save)
    print(f"Ranked {len(ranked_kebabs)} places.")

    # 5. Save to PocketBase
    count = 0
    for kebab in ranked_kebabs:
        try:
            print(f"Saving #{kebab.get('city_rank', 'N/A')} {kebab['name']} (Score: {kebab.get('rank_score', 0)})")
            pb_place_id = pb.upsert_kebab_place(
                google_place_id=kebab['google_place_id'],
                name=kebab['name'],
                address=kebab['address'],
                city_id=city_id,
                latitude=kebab['lat'],
                longitude=kebab['lng'],
                opening_hours=kebab.get('opening_hours'),
                photo_url=kebab.get('photo'),
            )
            pb.insert_rating_history(
                kebab_place_id=pb_place_id,
                rating=kebab['rating'],
                total_reviews=kebab['total_reviews'],
                positive_percentage=0,
                rank_score=kebab['rank_score'],
                city_rank=kebab['city_rank']
            )
            if kebab['google_place_id'] not in existing_ids_before:
                report_new.append({'name': kebab['name'], 'google_place_id': kebab['google_place_id']})
                print(f"    🆕 New place detected: {kebab['name']}")
            count += 1
        except Exception as e:
            print(f"Error saving {kebab['name']}: {e}")

    print(f"✓ Saved {count} records for {city_name}.")

    # 6. Detect disappeared places: were in DB before, not in this update, not in closed reports
    saved_ids = {kebab['google_place_id'] for kebab in ranked_kebabs}
    closed_ids = {p['google_place_id'] for p in report_closed_temp + report_closed_perm}
    report_disappeared = []
    for ep in existing_places:
        g_id = getattr(ep, 'google_place_id', '')
        if g_id and g_id not in saved_ids and g_id not in closed_ids:
            report_disappeared.append({'name': ep.name, 'google_place_id': g_id})
            print(f"  👻 Disappeared from search: {ep.name}")

    # 7. Save update report
    report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'update_reports')
    os.makedirs(report_dir, exist_ok=True)
    report = {
        'city': city_name,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'timestamp': datetime.now().isoformat(),
        'total_active': count,
        'new_places': report_new,
        'closed_temporarily': report_closed_temp,
        'closed_permanently': report_closed_perm,
        'disappeared_from_search': report_disappeared,
    }
    report_path = os.path.join(report_dir, f"{city_name}_{datetime.now().strftime('%Y-%m-%d')}.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n📊 Raport zapisany: {report_path}")
    print(f"   🆕 Nowe miejsca:          {len(report_new)}")
    print(f"   ⏸️  Tymczasowo zamknięte:  {len(report_closed_temp)}")
    print(f"   🔒 Na stałe zamknięte:    {len(report_closed_perm)}")
    print(f"   👻 Zniknęły z wyszukiwarki: {len(report_disappeared)}")


if __name__ == "__main__":
    import argparse
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("city", nargs="?", default="Zakopane")
    parser.add_argument("--limit", type=int, default=10, help="Ignored, backwards compat")
    args = parser.parse_args()

    update_city(
        args.city,
        os.getenv('DATAFORSEO_LOGIN'),
        os.getenv('DATAFORSEO_PASSWORD'),
    )
