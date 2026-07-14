import requests
import json

api_key = "ZUaHNRMieiVzFcAOvmyZ6tMjK9U4HDLN4MVejoLgmyn0K7LB"

# Search for a high-profile place to see many results/details
url = "https://cloud.gmapsextractor.com/api/v2/search"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "q": "Eiffel Tower",
    "page": 1,
    "extra": True,
    "ll": "@48.8583701,2.2922926,17z",
    "hl": "en",
    "gl": "fr"
}

print("Searching for Eiffel Tower with extra=True...")
r = requests.post(url, headers=headers, json=payload, timeout=20)
if r.status_code == 200:
    data = r.json()
    first = data.get('data', [])[0]
    print(f"Name: {first.get('Name')}")
    print(f"Keys: {first.keys()}")
    
    # Check if ANY key contains "Review" or looks like reviews list
    review_keys = [k for k in first.keys() if "Review" in k or "review" in k]
    print(f"Review-related keys: {review_keys}")
    
    # Is there a "Reviews" key with actual list?
    if "Reviews" in first:
        print(f"Reviews found! Count: {len(first['Reviews'])}")
        # print(json.dumps(first['Reviews'][0], indent=2))
    else:
        print("No internal 'Reviews' list found in search results.")
else:
    print(f"Search failed with {r.status_code}")
