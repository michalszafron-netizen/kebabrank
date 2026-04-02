import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService
from datetime import datetime
load_dotenv()

db = PocketbaseService(os.getenv('PB_URL'), os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))

print("=== VERIFYING CITY TREND LOGIC ===")
# Note: Since we only have one batch today, they should all be neutral/False for now
krakow = db.get_city_rankings("Kraków", limit=5)
for r in krakow:
    print(f"  {r['name'][:30]:<30} | Trend: {r['rank_change_indicator']} ({r['rank_change']}) | New: {r['is_new']}")

print("\n=== VERIFYING GLOBAL TREND LOGIC (Refresh) ===")
# Run population to see if it handles 'existing' data now (will be neutral first run)
os.system("python populate_global_top.py")

print("\n=== GLOBAL TOP 10 WITH TREND FIELDS ===")
global_top = db.get_global_rankings(limit=10)
for r in global_top:
    indicator = r.get('rank_change_indicator', '-')
    change = r.get('rank_change', 0)
    is_new = r.get('is_new', False)
    print(f"  #{r.get('global_rank'):>2}. {r['name'][:30]:<30} | {indicator:<8} ({change}) | NEW: {is_new}")
