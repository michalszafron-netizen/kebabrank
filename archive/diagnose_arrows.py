"""Diagnose arrow badge distribution for a city."""
import os, io, sys
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def diagnose_arrows(city_name):
    load_dotenv()
    pb = PocketbaseService(os.getenv("PB_URL"), os.getenv("PB_EMAIL"), os.getenv("PB_PASSWORD"))
    
    rankings = pb.get_city_rankings(city_name, limit=50)
    
    up = [r for r in rankings if r['rank_change_indicator'] == 'up']
    down = [r for r in rankings if r['rank_change_indicator'] == 'down']
    neutral = [r for r in rankings if r['rank_change_indicator'] == 'neutral' and not r['is_new']]
    new = [r for r in rankings if r['is_new']]
    
    print(f"=== {city_name} — Badge Distribution ===")
    print(f"Total places: {len(rankings)}")
    print(f"  🟢 UP:      {len(up)}")
    print(f"  🔴 DOWN:    {len(down)}")
    print(f"  ⚪ NEUTRAL: {len(neutral)}")
    print(f"  🆕 NEW:     {len(new)}")
    print()
    
    if up:
        print("UP arrows:")
        for r in up:
            print(f"  #{rankings.index(r)+1} {r['name']} (change: +{r['rank_change']})")
    if down:
        print("DOWN arrows:")
        for r in down:
            print(f"  #{rankings.index(r)+1} {r['name']} (change: {r['rank_change']})")
    if new:
        print("NEW badges:")
        for r in new:
            print(f"  #{rankings.index(r)+1} {r['name']}")
    if neutral:
        print("NEUTRAL:")
        for r in neutral:
            print(f"  #{rankings.index(r)+1} {r['name']}")

if __name__ == "__main__":
    city = sys.argv[1] if len(sys.argv) > 1 else "Tychy"
    diagnose_arrows(city)
