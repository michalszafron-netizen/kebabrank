import os
import sys
import io
import json
from dotenv import load_dotenv
from services.gmaps_extractor import GmapsextractorService

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def debug_city_results(city_name):
    load_dotenv()
    api_key = os.getenv('GMAPS_EXTRACTOR_API_KEY') or "ZUaHNRMieiVzFcAOvmyZ6tMjK9U4HDLN4MVejoLgmyn0K7LB"
    gmaps = GmapsextractorService(api_key)
    
    print(f"--- Debugging results for {city_name} ---")
    results = gmaps.search_places(f"kebab {city_name}", page=1)
    
    if not results:
        print("No results found.")
        return

    # Print relevant fields for the first 5 results
    for i, item in enumerate(results[:10]):
        print(f"\nResult #{i+1}:")
        print(f"Name: {item.get('Name')}")
        print(f"Fulladdress: {item.get('Fulladdress')}")
        print(f"Municipality: {item.get('Municipality')}")
        print(f"City: {item.get('City')}")
        print(f"Postal Code: {item.get('Postal Code') or item.get('Postcode')}")
        # Print all keys to see what's available
        # print(f"Available keys: {list(item.keys())}")

if __name__ == "__main__":
    debug_city_results("Tychy")
