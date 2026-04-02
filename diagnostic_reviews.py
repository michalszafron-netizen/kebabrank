import requests
import json

api_key = "ZUaHNRMieiVzFcAOvmyZ6tMjK9U4HDLN4MVejoLgmyn0K7LB"
place_id = "ChIJBZDymRbzFUcRnKoFtGu8kOA" # Siesta Burger

endpoints = [
    "https://cloud.gmapsextractor.com/api/v2/place/reviews",
    "https://cloud.gmapsextractor.com/api/v2/placeDetails",
    "https://cloud.gmapsextractor.com/api/v2/details",
    "https://cloud.gmapsextractor.com/api/reviews",
    "https://cloud.gmapsextractor.com/api/place/reviews",
    "https://cloud.gmapsextractor.com/api/v2/search/reviews"
]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "place_id": place_id,
    "limit": 5
}

for url in endpoints:
    print(f"Testing: {url}")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print(f"  SUCCESS! Keys: {response.json().keys()}")
            # print(json.dumps(response.json(), indent=2)[:500])
        elif response.status_code != 404:
            print(f"  Response: {response.text[:200]}")
    except Exception as e:
        print(f"  Error: {e}")
    print("-" * 20)
