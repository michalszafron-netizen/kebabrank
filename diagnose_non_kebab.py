"""Diagnose non-kebab places in the database by checking place names."""
import os, io, sys
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Keywords that STRONGLY suggest it IS a kebab place (whitelist)
KEBAB_KEYWORDS = [
    'kebab', 'kebap', 'kebap', 'doner', 'döner', 'dürüm', 'durum',
    'shawarma', 'szawarma', 'gyros', 'pita', 'falafel',
    'turkish', 'turecki', 'turecka', 'istanbul',
    'ali baba', 'sultan', 'efes', 'ankara', 'antalya',
]

# Keywords that suggest it is NOT a kebab place (blacklist)
NOT_KEBAB_KEYWORDS = [
    'sushi', 'ramen', 'pho', 'wok', 'china', 'chinski', 'chiński',
    'indian', 'indyjska', 'india', 'curry house',
    'steak', 'steakhouse',
    'ice cream', 'lody', 'cukiernia', 'bakery',
    'hotel', 'hostel', 'motel',
    'mcdonalds', 'kfc', 'subway', 'burger king',
    'apteka', 'pharmacy',
]

def diagnose():
    load_dotenv()
    pb = PocketbaseService(os.getenv("PB_URL"), os.getenv("PB_EMAIL"), os.getenv("PB_PASSWORD"))
    pb._ensure_auth()
    
    page = 1
    suspicious = []
    total = 0
    while True:
        results = pb.client.collection('kebab_places').get_list(page, 200)
        if not results.items:
            break
        for item in results.items:
            total += 1
            name_lower = item.name.lower()
            # Check if name contains any kebab keyword
            has_kebab_keyword = any(kw in name_lower for kw in KEBAB_KEYWORDS)
            # Check if name contains a blacklisted keyword
            has_blacklist = any(kw in name_lower for kw in NOT_KEBAB_KEYWORDS)
            
            if has_blacklist and not has_kebab_keyword:
                suspicious.append(item.name)
            elif not has_kebab_keyword:
                # Places that don't have ANY kebab keyword might be suspicious
                # but could be generic fast food names - flag them for review
                # Only flag if the name looks very non-kebab
                generic_food = any(kw in name_lower for kw in [
                    'pizza', 'burger', 'chicken', 'wings', 'naleśnik',
                    'pierogi', 'milk bar', 'bar mleczny', 'restauracja',
                    'bistro', 'grill', 'fast food', 'snack'
                ])
                if generic_food:
                    pass  # These COULD have kebab too, skip for now
        
        if page * 200 >= results.total_items:
            break
        page += 1
    
    print(f"Total places in database: {total}")
    print(f"\nSuspicious non-kebab places ({len(suspicious)}):")
    for name in sorted(suspicious):
        print(f"  - {name}")

if __name__ == "__main__":
    diagnose()
