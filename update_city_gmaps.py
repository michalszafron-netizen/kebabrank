import os
import sys
import io
from dotenv import load_dotenv
from services.gmaps_extractor import GmapsextractorService
from services.pocketbase_db import PocketbaseService
from services.ranking import RankingService
from datetime import datetime

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── Kebab Qualification Filter ──────────────────────────────────────────
# Name keywords that STRONGLY indicate a kebab place
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

# Name keywords that indicate NOT a kebab place (override only if NO whitelist match)
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

# Google Maps categories that indicate a kebab-related place
KEBAB_CATEGORY_WHITELIST = [
    'kebab', 'doner', 'döner', 'turkish', 'middle eastern',
    'fast food', 'shawarma', 'gyro', 'falafel', 'pita',
    'take out', 'takeaway', 'meal takeaway',
]

# Google Maps categories that indicate NOT a kebab place
KEBAB_CATEGORY_BLACKLIST = [
    'sushi', 'indian', 'chinese', 'japanese', 'thai', 'vietnamese',
    'steakhouse', 'ice cream', 'bakery', 'hotel', 'bar',
    'italian restaurant', 'french restaurant', 'spanish restaurant',
]

def is_kebab_place(item: dict) -> bool:
    """
    Strict kebab qualification filter.
    Returns True ONLY if there is positive evidence the place serves kebab.
    
    Rules:
    1. Name contains a kebab whitelist keyword → INCLUDE
    2. Name contains a blacklist keyword (and no whitelist) → EXCLUDE
    3. Google Maps categories contain a kebab-related category → INCLUDE
    4. Default → EXCLUDE (no evidence this is a kebab place)
    """
    name = (item.get('Name') or '').lower()
    categories = item.get('Categories', [])
    if not categories:
        categories = []
    categories_lower = ' '.join([c.lower() for c in categories])

    # Stage 1: Name-based check
    has_whitelist_name = any(kw in name for kw in KEBAB_NAME_WHITELIST)
    has_blacklist_name = any(kw in name for kw in KEBAB_NAME_BLACKLIST)

    # If name explicitly contains a kebab keyword, always include
    if has_whitelist_name:
        return True

    # If name contains a blacklist keyword (and no whitelist), reject immediately
    if has_blacklist_name:
        return False

    # Stage 2: Category-based check (for places with generic names like "Good Food")
    has_whitelist_cat = any(kw in categories_lower for kw in KEBAB_CATEGORY_WHITELIST)

    # If categories contain a kebab-related one, include
    if has_whitelist_cat:
        return True

    # DEFAULT: EXCLUDE — no evidence this is a kebab place
    # (Catches: "Tyska stołówka", "warzywniak", "Giovani", "Stacja Tychy Miasto", etc.)
    return False


def update_city_with_gmaps(city_name: str, api_key: str):
    load_dotenv()
    
    # 1. Initialize services
    gmaps = GmapsextractorService(api_key)
    pb = PocketbaseService(os.getenv('PB_URL'))
    ranker = RankingService()
    
    print(f"--- Updating {city_name} via Gmapsextractor ---")
    
    # 2. Get city ID
    city_id = pb.get_city_id(city_name)
    if not city_id:
        print(f"Error: City '{city_name}' not found in database.")
        return

    # NEW: Reset existing ranks for this city before update
    pb.reset_city_ranks(city_id)

    # 3. Search for kebabs in city
    # Gmapsextractor v2 API works best with coordinates (ll)
    ll = None
    try:
        # Try to get coordinates from an existing place in this city
        sample_place = pb.client.collection('kebab_places').get_first_list_item(f'city="{city_id}"')
        if sample_place and getattr(sample_place, 'lat', None):
            ll = f"@{sample_place.lat},{sample_place.lng},13z"
            print(f"Using coordinates for {city_name}: {ll}")
    except:
        pass

    query = f"kebab" # Just 'kebab' if using coords
    if not ll:
        query = f"kebab {city_name}"
        
    print(f"Searching Google Maps for: '{query}'...")
    all_results = []
    for p in range(1, 5): # Fetch up to 3 pages (60 places)
        print(f"Fetching page {p}...")
        results = gmaps.search_places(query, page=p, extra=True, ll=ll)
        if not results:
            break
        all_results.extend(results)
        if len(results) < 20: # Gmapsextractor usually returns 20 per page
            break
    
    if not all_results:
        print("No results found or API error.")
        return

    # NEW LOGIC: Prevent dropping existing places due to Google pagination limits!
    # Instead of losing top places, we cross-check with what we already have in the database.
    # If the broad search missed a place we already know about, we explicitly query for it.
    
    found_google_ids = {item.get('Place Id') for item in all_results if item.get('Place Id')}
    
    print(f"Cross-checking against existing database to catch skipped places...")
    existing_places = pb.client.collection('kebab_places').get_full_list(
        query_params={"filter": f'city="{city_id}"'}
    )
    
    missed_count = 0
    for ep in existing_places:
        g_id = getattr(ep, 'google_place_id', '')
        if g_id and g_id not in found_google_ids:
            # Google's general search missed it. Let's explicitly search for it to update its stats!
            print(f"  Explicitly fetching missing known place: {ep.name}")
            # Search by specific name and city
            try:
                explicit_results = gmaps.search_places(f"{ep.name} {city_name}", page=1, extra=True, ll=ll)
                
                if explicit_results:
                    # Find the exact match
                    for raw_item in explicit_results:
                        if raw_item.get('Place Id') == g_id:
                            all_results.append(raw_item)
                            found_google_ids.add(g_id)
                            missed_count += 1
                            print(f"    ✓ Found and updated: {ep.name}")
                            break
            except Exception as e:
                print(f"    Failed to fetch {ep.name}: {e}")

    print(f"Found {len(all_results)} places total ({missed_count} recovered from explicit search). Processing...")

    # 4. Filter and prepare data
    places_to_save = []
    skipped_non_kebab = 0
    seen_ids = set() # For deduplication
    for item in all_results:
        # Gmapsextractor v2 API response keys (case-sensitive)
        g_id = item.get('Place Id')
        if not g_id or g_id in seen_ids:
            continue
        seen_ids.add(g_id)
            
        import re
        full_address = item.get('Fulladdress', '')
        # Smart city filter: find the address chunk containing Polish postal code (XX-XXX).
        # That chunk contains the REAL city name, e.g. "41-800 Zabrze" or "41-506 Chorzów".
        # This ignores misleading country suffixes like "..., Stany Zjednoczone, Chorzów"
        # or neighboring city names appended at the end by Google Maps.
        parts = [p.strip() for p in full_address.split(',')]
        city_chunk = None
        for part in parts:
            if re.search(r'\b\d{2}-\d{3}\b', part):
                city_chunk = part.lower()
                break

        if city_chunk is None:
            # No Polish postal code at all - foreign address (Los Angeles etc.)
            print(f"  ⛔ Skipping {item.get('Name')} - No Polish postal code (Address: {full_address})")
            continue

        if city_name.lower() not in city_chunk:
            print(f"  ⛔ Skipping {item.get('Name')} - Not in {city_name} (Postal chunk: {city_chunk})")
            continue
        # Kebab Qualification Filter:
        if not is_kebab_place(item):
            cats = item.get('Categories', [])
            print(f"  🚫 Skipping {item.get('Name')} - Not a kebab place (Categories: {cats})")
            skipped_non_kebab += 1
            continue

        place_data = {
            'name': item.get('Name'),
            'address': full_address,
            'google_place_id': g_id,
            'rating': float(item.get('Average Rating') or 0),
            'total_reviews': int(item.get('Review Count') or 0),
            'lat': float(item.get('Latitude') or 0),
            'lng': float(item.get('Longitude') or 0)
        }
        places_to_save.append(place_data)
    
    if skipped_non_kebab > 0:
        print(f"  ℹ️ Filtered out {skipped_non_kebab} non-kebab places.")

    # 5. Rank the kebabs (to get current city_rank)
    ranked_kebabs = ranker.rank_kebabs(places_to_save)
    print(f"Ranked {len(ranked_kebabs)} places.")

    # 6. Save to PocketBase
    # We insert into 'kebab_places' (upsert) and then 'ratings' (new history record)
    count = 0
    for kebab in ranked_kebabs:
        try:
            print(f"Saving #{kebab.get('city_rank', 'N/A')} {kebab['name']} (Score: {kebab.get('rank_score', 0)})")
            # a. Upsert place
            pb_place_id = pb.upsert_kebab_place(
                google_place_id=kebab['google_place_id'],
                name=kebab['name'],
                address=kebab['address'],
                city_id=city_id,
                latitude=kebab['lat'],
                longitude=kebab['lng']
            )
            
            # b. Insert rating history (this creates the 'arrow' logic foundation)
            pb.insert_rating_history(
                kebab_place_id=pb_place_id,
                rating=kebab['rating'],
                total_reviews=kebab['total_reviews'],
                positive_percentage=0, # Ignored in ranking logic
                rank_score=kebab['rank_score'],
                city_rank=kebab['city_rank']
            )
            count += 1
        except Exception as e:
            print(f"Error saving {kebab['name']}: {e}")

    print(f"✓ Saved {count} records for {city_name}.")
    print(f"The rankings will now show trends (arrows) when compared to the previous update.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("city", nargs="?", default="Zakopane")
    parser.add_argument("--key", default="ZUaHNRMieiVzFcAOvmyZ6tMjK9U4HDLN4MVejoLgmyn0K7LB")
    parser.add_argument("--limit", type=int, default=10, help="Ignored, just for backwards compat")
    args = parser.parse_args()
    
    update_city_with_gmaps(args.city, args.key)
