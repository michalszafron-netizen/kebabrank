import os, sys, io
from dotenv import load_dotenv
from pocketbase import PocketBase

# Fix encoding for Polish characters like ł, ś, ą in Windows terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()
pb = PocketBase(os.getenv('PB_URL'))
pb.admins.auth_with_password(os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))

# 1. Get all cities
cities = pb.collection('cities').get_full_list()
city_map = {c.id: c.name for c in cities}

# 2. Get counts per city from kebab_places
all_places = pb.collection('kebab_places').get_full_list()

stats = {}
for p in all_places:
    city_name = city_map.get(p.city, "Unknown")
    stats[city_name] = stats.get(city_name, 0) + 1

# 3. Sort by count descending then name
sorted_stats = sorted(stats.items(), key=lambda x: (-x[1], x[0]))

print("| City | Places Count |")
print("| :--- | :--- |")
for city, count in sorted_stats:
    print(f"| {city} | {count} |")

print(f"\n**Total Unique Places**: {len(all_places)}")
print(f"**Total Cities**: {len(stats)}")
