import os
import sys
import io
import argparse
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService
import subprocess

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_updates(cities=None, all_cities=False, ai_limit=10, run_ai=True):
    load_dotenv()
    pb = PocketbaseService(os.getenv('PB_URL'), os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))

    target_cities = []

    if all_cities:
        print("Fetching all cities from database...")
        records = pb.client.collection('cities').get_full_list()
        target_cities = [r.name for r in records]
    elif cities:
        target_cities = cities  # fuzzy matching handled in get_city_id
    else:
        print("Error: No cities specified. Use --city Name or --all.")
        return

    print(f"Target cities for update: {', '.join(target_cities)}")
    print("-" * 30)

    for city in target_cities:
        print(f"\n>>> PROCESSING CITY: {city.upper()} <<<")
        
        # 1. Update GMaps Data (Rankings, Arrows, New entries)
        print(f"\nStep 1: Updating GMaps data and base rankings...")
        try:
            subprocess.run([sys.executable, "update_city_gmaps.py", city], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error updating GMaps for {city}: {e}")
            continue

        # 2. Update AI Analysis
        if run_ai:
            print(f"\nStep 2: Running AI Analysis (Top {ai_limit})...")
            try:
                subprocess.run([sys.executable, "update_city_review_ai.py", city, "--limit", str(ai_limit)], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running AI analysis for {city}: {e}")
                continue

    print("\n" + "=" * 30)
    print("ALL UPDATES COMPLETED SUCCESSFULLY")
    print("=" * 30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Elastic Kebab Update Script")
    parser.add_argument('--city', nargs='+', help='One or more cities to update (e.g. --city Tychy Zakopane)')
    parser.add_argument('--all', action='store_true', help='Update ALL cities in the database')
    parser.add_argument('--limit', type=int, default=10, help='AI analysis limit (default: 10)')
    parser.add_argument('--no-ai', action='store_false', dest='run_ai', help='Skip AI analysis')
    
    args = parser.parse_args()
    
    run_updates(cities=args.city, all_cities=args.all, ai_limit=args.limit, run_ai=args.run_ai)
