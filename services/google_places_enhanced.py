# services/google_places_enhanced.py
import googlemaps
from typing import List, Dict, Optional
import time
from datetime import datetime

class GooglePlacesEnhancedService:
    def __init__(self, api_key: str):
        self.gmaps = googlemaps.Client(key=api_key)
        self.base_service = googlemaps.Client(key=api_key)
    
    def get_place_reviews(self, place_id: str, max_reviews: int = 100) -> List[Dict]:
        """
        Fetch reviews for a specific place
        Note: Google Places API typically returns up to 5 reviews only
        For more reviews, you'd need Google My Business API (requires verification)
        """
        try:
            # Get place details including reviews
            result = self.gmaps.place(
                place_id=place_id,
                fields=['name', 'rating', 'user_ratings_total', 'reviews'],
                language='pl'  # Get Polish reviews first
            )
            
            place_data = result.get('result', {})
            reviews = place_data.get('reviews', [])
            
            # Also try to get English reviews
            try:
                result_en = self.gmaps.place(
                    place_id=place_id,
                    fields=['reviews'],
                    language='en'
                )
                reviews_en = result_en.get('result', {}).get('reviews', [])
                
                # Merge unique reviews
                existing_authors = {r['author_name'] for r in reviews}
                for review in reviews_en:
                    if review['author_name'] not in existing_authors:
                        reviews.append(review)
            except:
                pass
            
            # Format reviews for AI analysis
            formatted_reviews = []
            for review in reviews[:max_reviews]:
                formatted_reviews.append({
                    'author_name': review.get('author_name', 'Anonymous'),
                    'rating': review.get('rating', 3),
                    'text': review.get('text', ''),
                    'time': datetime.fromtimestamp(review.get('time', 0)),
                    'language': review.get('language', 'pl'),
                    'profile_photo_url': review.get('profile_photo_url', ''),
                    'relative_time': review.get('relative_time_description', '')
                })
            
            return formatted_reviews
            
        except Exception as e:
            print(f"Error fetching reviews for place {place_id}: {e}")
            return []
    
    def get_place_insights(self, place_id: str) -> Dict:
        """Get additional insights about a place"""
        try:
            result = self.gmaps.place(
                place_id=place_id,
                fields=['opening_hours', 'price_level', 'types', 'website', 
                       'formatted_phone_number', 'business_status']
            )
            
            place = result.get('result', {})
            
            # Extract useful insights
            insights = {
                'is_open_now': place.get('opening_hours', {}).get('open_now', None),
                'price_level': place.get('price_level', 2),  # 1-4 scale
                'types': place.get('types', []),
                'website': place.get('website', ''),
                'phone': place.get('formatted_phone_number', ''),
                'business_status': place.get('business_status', 'OPERATIONAL'),
                'weekly_hours': place.get('opening_hours', {}).get('weekday_text', [])
            }
            
            return insights
            
        except Exception as e:
            print(f"Error fetching insights for place {place_id}: {e}")
            return {}
    
    def search_kebabs_with_reviews(self, city_name: str) -> List[Dict]:
        """Enhanced search that includes review data"""
        kebab_places = []
        
        search_queries = [
            f"kebab {city_name} Poland",
            f"kebap {city_name} Poland",
            f"döner {city_name} Poland"
        ]
        
        seen_place_ids = set()
        
        for query in search_queries:
            try:
                results = self.gmaps.places(
                    query=query,
                    type='restaurant',
                    language='pl'
                )
                
                for place in results.get('results', []):
                    place_id = place['place_id']
                    
                    if place_id in seen_place_ids:
                        continue
                    
                    name_lower = place['name'].lower()
                    if not self._is_kebab_place(name_lower):
                        continue
                    
                    seen_place_ids.add(place_id)
                    
                    # Get basic details
                    kebab_data = {
                        'place_id': place_id,
                        'name': place.get('name'),
                        'address': place.get('formatted_address'),
                        'location': place.get('geometry', {}).get('location'),
                        'rating': place.get('rating', 0),
                        'total_reviews': place.get('user_ratings_total', 0),
                        'types': place.get('types', [])
                    }
                    
                    # Add review count for AI analysis priority
                    kebab_data['has_reviews'] = kebab_data['total_reviews'] > 0
                    
                    kebab_places.append(kebab_data)
                    
                # Limit to prevent API overuse
                if len(kebab_places) >= 50:
                    break
                    
            except Exception as e:
                print(f"Error searching with query '{query}': {e}")
                continue
        
        return kebab_places
    
    def _is_kebab_place(self, name: str) -> bool:
        """Check if the place name indicates it's a kebab restaurant"""
        kebab_keywords = ['kebab', 'kebap', 'döner', 'doner', 'shawarma', 'gyros','polenezrestauracja']
        exclude_keywords = ['pizza', 'burger', 'sushi', 'chinese', 'thai', 'italian']
        
        has_kebab = any(keyword in name for keyword in kebab_keywords)
        is_excluded = any(keyword in name and keyword not in kebab_keywords 
                         for keyword in exclude_keywords)
        
        return has_kebab and not is_excluded