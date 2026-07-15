import requests
from typing import List, Dict, Optional
from requests.exceptions import RequestException

class GmapsextractorService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://cloud.gmapsextractor.com/api/v2"

    def search_places(self, query: str, page: int = 1, extra: bool = True, ll: str = None) -> List[Dict]:
        """
        Search for places on Google Maps using Gmapsextractor API.
        Returns a list of place dictionaries.
        ll format: "@lat,lng,zoomz" e.g. "@49.299181,19.949285,13z"
        """
        url = f"{self.base_url}/search"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "page": page,
            "hl": "pl",
            "gl": "pl",
        }
        if extra:
            payload["extra"] = True
        if ll:
            payload["ll"] = ll

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Based on successful test, data is in "data" key
            if isinstance(data, dict):
                return data.get('data', [])
            return []
        except RequestException as e:
            print(f"Gmapsextractor API Error: {e}")
            if e.response is not None:
                print(f"Details: {e.response.text}")
            return []
        except Exception as e:
            print(f"Gmapsextractor Unexpected Error: {e}")
            return []

    def get_place_reviews(self, google_place_id: str, limit: int = 20, max_reviews: int = None) -> List[Dict]:
        """
        Fetch reviews for a specific place using Gmapsextractor API.
        """
        if max_reviews is not None:
            limit = max_reviews
            
        url = f"{self.base_url}/reviews"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "place_id": google_place_id,
            "limit": limit
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Based on documentation, reviews are often under "data"
            if isinstance(data, dict):
                reviews = data.get('data', [])
                # Format to match internal expectations (similar to Google Service)
                formatted = []
                for r in reviews:
                    # Gmapsextractor field names (Review Text, Review Rating, etc.)
                    formatted.append({
                        'author_name': r.get('Review Author', 'Anonymous'),
                        'rating': r.get('Review Rating', 3),
                        'text': r.get('Review Text', ''),
                        'time': r.get('Review Date', ''), # We'll keep as string or try to parse
                    })
                return formatted
            return []
        except Exception as e:
            print(f"Gmapsextractor Reviews Error: {e}")
            return []
