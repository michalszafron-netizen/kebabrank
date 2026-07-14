import os
import sys
import io
import json
import requests
from dotenv import load_dotenv

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def dump_zakopane_raw():
    load_dotenv()
    api_key = os.getenv('GMAPS_EXTRACTOR_API_KEY') or "ZUaHNRMieiVzFcAOvmyZ6tMjK9U4HDLN4MVejoLgmyn0K7LB"
    url = "https://cloud.gmapsextractor.com/api/v2/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "q": "kebab Zakopane",
        "page": 1,
        "extra": True
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get('data'):
            first_item = data['data'][0]
            print("Keys in Gmapsextractor result:")
            print(json.dumps(list(first_item.keys()), indent=2))
            print("\nSample values for potential image fields:")
            for key in first_item.keys():
                if any(x in key.lower() for x in ['image', 'photo', 'url', 'thumb', 'media']):
                    print(f"  {key}: {first_item[key]}")
        else:
            print("No data found in response.")
            print(json.dumps(data, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    dump_zakopane_raw()
