import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class SerperService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://google.serper.dev/reviews"
        
    def get_place_reviews(self, place_id: str, max_reviews: int = 100) -> List[Dict]:
        """Fetch reviews for a place using Serper.dev"""
        if not self.api_key:
            print("  Error: No Serper API key provided")
            return []
            
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        all_reviews = []
        next_page_token = None
        
        # Limit to 5 pages (approx 50-100 reviews) to save credits and time
        max_pages = (max_reviews + 9) // 10
        pages_fetched = 0
        
        while pages_fetched < max_pages:
            payload = {
                "placeId": place_id,
                "gl": "pl",
                "hl": "pl",
                "sortBy": "newest"
            }
            if next_page_token:
                payload["nextPageToken"] = next_page_token
                
            try:
                response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
                if response.status_code != 200:
                    print(f"  Error: Serper API returned {response.status_code}")
                    break
                    
                data = response.json()
                reviews = data.get('reviews', [])
                
                for r in reviews:
                    # Format for AIKebabAnalyzer
                    formatted = {
                        'author_name': r.get('user', {}).get('name', 'Anonymous'),
                        'rating': r.get('rating', 3),
                        'text': r.get('snippet', ''),
                        'time': self._parse_date(r.get('isoDate')),
                        'language': 'pl' if 'translatedSnippet' not in r else 'en' # Simplified
                    }
                    all_reviews.append(formatted)
                    
                next_page_token = data.get('nextPageToken')
                pages_fetched += 1
                
                if not next_page_token or len(all_reviews) >= max_reviews:
                    break
                    
            except Exception as e:
                print(f"  Exception fetching reviews from Serper: {e}")
                break
                
        return all_reviews[:max_reviews]
        
    def _parse_date(self, iso_string: Optional[str]) -> datetime:
        """Parse ISO date string to datetime object"""
        if not iso_string:
            return datetime.now()
        try:
            # Serper isoDate is like "2024-03-01T20:58:31.715Z"
            # Replace Z with +00:00 for fromisoformat if needed, but modern python handled it
            # Actually Z is best handled by .replace('Z', '+00:00')
            cleaned = iso_string.replace('Z', '+00:00')
            return datetime.fromisoformat(cleaned)
        except:
            return datetime.now()
