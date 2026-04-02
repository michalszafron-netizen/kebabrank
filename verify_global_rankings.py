import requests
import json

def verify_global_rankings():
    """Verify that global rankings are sorted correctly across cities."""
    print("Testing Global Rankings (TOP 10 w Polsce)...")
    
    try:
        response = requests.get('http://localhost:5000/api/rankings/global')
        if response.status_code != 200:
            print(f"❌ Error: API returned status {response.status_code}")
            return

        data = response.json()
        rankings = data.get('data', [])
        
        if not rankings:
            print("❌ Error: No global rankings found.")
            return

        print(f"✓ Found {len(rankings)} global rankings.")
        
        last_score = float('inf')
        is_sorted = True
        cities_found = set()
        
        for i, kebab in enumerate(rankings):
            name = kebab.get('name')
            city = kebab.get('city')
            score = kebab.get('rank_score', 0)
            cities_found.add(city)
            
            print(f"{i+1}. [{city}] {name} - Score: {score}")
            
            if score > last_score:
                is_sorted = False
                print(f"   ⚠️ ERROR: Out of order! {score} > {last_score}")
            
            last_score = score

        if is_sorted:
            print("\n✅ SUCCESS: Global rankings are correctly sorted by rank_score.")
        else:
            print("\n❌ FAILURE: Global rankings are NOT sorted correctly.")
            
        print(f"✓ Cities represented in Top 10: {', '.join(cities_found)}")

    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    verify_global_rankings()
