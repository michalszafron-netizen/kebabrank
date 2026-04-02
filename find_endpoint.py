import requests
import json

api_key = "ZUaHNRMieiVzFcAOvmyZ6tMjK9U4HDLN4MVejoLgmyn0K7LB"
place_id = "ChIJBZDymRbzFUcRnKoFtGu8kOA" # Siesta Burger

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Try some variants and also check if there's any info at root
base_variants = [
    "https://cloud.gmapsextractor.com/api/v2",
    "https://cloud.gmapsextractor.com/api"
]

print("--- Checking Roots ---")
for base in base_variants:
    try:
        r = requests.get(base, headers=headers, timeout=10)
        print(f"GET {base}: {r.status_code}")
        # if r.status_code == 200: print(r.text[:500])
    except: pass

print("\n--- Testing Potential Endpoints ---")
paths = [
    "/reviews",
    "/search/reviews",
    "/place/reviews",
    "/business/reviews",
    "/reviews/search",
    "/reviews/get",
    "/place_details",
    "/place-details",
    "/details"
]

for base in base_variants:
    for path in paths:
        url = base + path
        print(f"POST {url}")
        try:
            # Try both JSON payload formats
            for payload in [{"place_id": place_id}, {"q": place_id}, {"id": place_id}]:
                r = requests.post(url, headers=headers, json=payload, timeout=5)
                if r.status_code == 200:
                    print(f"  SUCCESS! URL: {url} Payload: {payload}")
                    print(f"  Keys: {r.json().keys()}")
                    exit(0)
                elif r.status_code != 404:
                    print(f"  Status {r.status_code} for {payload}")
        except: pass
