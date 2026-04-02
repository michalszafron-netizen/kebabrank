
import os
import json
from dotenv import load_dotenv
from services.gmaps_extractor import GmapsextractorService

def debug_gmaps_fields():
    load_dotenv()
    api_key = os.getenv("GMAPS_EXTRACTOR_API_KEY")
    if not api_key:
        # Hardcoded for test if env fails
        api_key = "ZUaHNRMieiVzFcAOvmyZ6tMjK9U4HDLN4MVejoLgmyn0K7LB"
        
    gmaps = GmapsextractorService(api_key)
    print("Searching for kebab in Zakopane...")
    results = gmaps.search_places("kebab Zakopane", page=1, extra=True)
    
    if results:
        print(f"Found {len(results)} results.")
        # Dump the first result to see all keys
        first = results[0]
        print("\n--- SAMPLE RESULT FIELDS ---")
        for key, value in first.items():
            print(f"{key}: {value}")
            
        # specifically look for category/type/keywords
        print("\n--- CATEGORY RELATED FIELDS ---")
        cat_keys = [k for k in first.keys() if any(x in k.lower() for x in ['cat', 'type', 'key', 'tag', 'desc'])]
        for k in cat_keys:
            print(f"{k}: {first[k]}")
            
        # Save one to file for deeper inspection
        with open("sample_gmaps_result.json", "w", encoding='utf-8') as f:
            json.dump(first, f, indent=4, ensure_ascii=False)
    else:
        print("No results found.")

if __name__ == "__main__":
    debug_gmaps_fields()
