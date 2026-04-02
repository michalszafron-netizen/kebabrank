# services/google_places.py
import googlemaps
from typing import List, Dict
import time

class GooglePlacesService:
    def __init__(self, api_key: str):
        self.gmaps = googlemaps.Client(key=api_key)
        
    def search_kebabs_in_city(self, city_name: str) -> List[Dict]:
        """Search for kebab places in a specific city"""
        kebab_places = []
        
        # Search queries to find kebab places
        search_queries = [
            f"kebab {city_name} Poland",
            f"kebap {city_name} Poland",
            f"döner {city_name} Poland",
            f"doner {city_name} Poland",
            f"shawarma {city_name} Poland",
            f"wrap {city_name} Poland",
            f"shawerma {city_name} Poland",
            f"Polenez Turecka {city_name} Poland",
            f"Polenezrestauracja {city_name} Poland",
            f"gyros {city_name} Poland"
        ]
        
        seen_place_ids = set()
        
        print(f"🔍 Searching for kebabs in {city_name}...")
        
        for query in search_queries:
            try:
                # Text search for kebab places
                results = self.gmaps.places(
                    query=query,
                    type='restaurant',
                    language='pl'
                )
                
                for place in results.get('results', []):
                    place_id = place['place_id']
                    
                    # Skip if already processed
                    if place_id in seen_place_ids:
                        continue
                    
                    # Filter out non-kebab places
                    name_lower = place['name'].lower()
                    if not self._is_kebab_place(name_lower):
                        continue
                    
                    seen_place_ids.add(place_id)
                    
                    # Get detailed information with city validation
                    details = self._get_place_details(place_id, city_name)
                    if details:
                        kebab_places.append(details)
                        print(f"  ✅ Added '{details['name']}' from {details.get('actual_city', 'unknown')}")
                
                # Handle pagination
                next_page_token = results.get('next_page_token')
                while next_page_token and len(kebab_places) < 60:
                    time.sleep(2)  # Required delay for pagination
                    results = self.gmaps.places(page_token=next_page_token)
                    
                    for place in results.get('results', []):
                        place_id = place['place_id']
                        if place_id in seen_place_ids:
                            continue
                        
                        name_lower = place['name'].lower()
                        if not self._is_kebab_place(name_lower):
                            continue
                        
                        seen_place_ids.add(place_id)
                        details = self._get_place_details(place_id, city_name)
                        if details:
                            kebab_places.append(details)
                            print(f"  ✅ Added '{details['name']}' from {details.get('actual_city', 'unknown')}")
                    
                    next_page_token = results.get('next_page_token')
                    
            except Exception as e:
                print(f"Error searching with query '{query}': {e}")
                continue
        
        print(f"📊 Found {len(kebab_places)} valid kebabs in {city_name}")
        return kebab_places
    
    def _is_kebab_place(self, name: str) -> bool:
        """Check if the place name indicates it's a kebab restaurant"""
        kebab_keywords = ['kebab', 'kebap', 'döner', 'doner', 'shawarma', 'gyros', 'wrap','shawerma','turkish','Polenez Turecka','Kebab', 'Kebap', 'Döner', 'Doner', 'Shawarma', 'Gyros', 'Wrap','Shawerma','Turkish','polenez turecka']
        exclude_keywords = ['pizza', 'burger', 'sushi', 'chinese', 'thai', 'italian', 'Pizza', 'Burger', 'Sushi', 'Chinese', 'Thai', 'Italian' ]
        
        # Must contain at least one kebab keyword
        has_kebab = any(keyword in name for keyword in kebab_keywords)
        
        # Should not be primarily another type of restaurant
        is_excluded = any(keyword in name and keyword not in kebab_keywords 
                         for keyword in exclude_keywords)
        
        return has_kebab and not is_excluded
    
    def _get_place_details(self, place_id: str, target_city: str = None) -> Dict:
        """Get detailed information about a place"""
        try:
            result = self.gmaps.place(
                place_id=place_id,
                fields=['name', 'formatted_address', 'geometry', 'rating', 
                       'user_ratings_total', 'review', 'type', 'business_status', 'photos']
            )
            
            place = result.get('result', {})
            
            # If the place is permanently closed, ignore it.
            if place.get('business_status') == 'CLOSED_PERMANENTLY':
                print(f"  ❌ Skipping '{place.get('name')}' - Permanently Closed")
                return None
            
            # Extract city from address and validate if target_city is provided
            address = place.get('formatted_address', '')
            actual_city = self._extract_city_from_address(address)
            
            # If target_city is provided, validate that the place is actually in that city
            if target_city and actual_city:
                if not self._is_city_match(target_city, actual_city):
                    print(f"  ⚠️  Skipping '{place.get('name')}' - located in {actual_city}, not {target_city}")
                    return None
            
            # Calculate positive review percentage based on rating
            # Since we can't get individual reviews, estimate based on rating
            rating = place.get('rating', 0)
            if rating >= 4.8:
                positive_percentage = 95.0
            elif rating >= 4.5:
                positive_percentage = 90.0
            elif rating >= 4.2:
                positive_percentage = 85.0
            elif rating >= 4.0:
                positive_percentage = 80.0
            elif rating >= 3.5:
                positive_percentage = 70.0
            else:
                positive_percentage = 60.0
            
            # Extract photo reference
            photos = place.get('photos', [])
            photo_url = photos[0].get('photo_reference') if photos else None
            
            return {
                'place_id': place_id,
                'name': place.get('name'),
                'address': place.get('formatted_address'),
                'location': place.get('geometry', {}).get('location'),
                'rating': place.get('rating', 0),
                'total_reviews': place.get('user_ratings_total', 0),
                'positive_percentage': positive_percentage,
                'types': place.get('type', []),
                'actual_city': actual_city,
                'photo_url': photo_url
            }
            
        except Exception as e:
            print(f"Error getting details for place {place_id}: {e}")
            return None
    
    def _extract_city_from_address(self, address: str) -> str:
        """Extract city name from formatted address"""
        if not address:
            return None
        
        # Common Polish address patterns
        address_lower = address.lower()
        
        # Look for city name after postal code pattern (e.g., "43-200 Pszczyna")
        import re
        postal_code_pattern = r'\d{2}-\d{3}\s+([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ\s-]+)(?:,|$)'
        match = re.search(postal_code_pattern, address)
        if match:
            city = match.group(1).strip()
            return city
        
        # Look for city at the end of address (common pattern)
        parts = address.split(',')
        if len(parts) >= 2:
            # Try the last part (usually country/city)
            last_part = parts[-1].strip()
            if 'poland' not in last_part.lower() and len(last_part) > 2:
                return last_part
        
        # Try second to last part
        if len(parts) >= 3:
            city_part = parts[-2].strip()
            if len(city_part) > 2:
                return city_part
        
        return None
    
    def _is_city_match(self, target_city: str, actual_city: str) -> bool:
        """Check if the actual city matches the target city"""
        if not target_city or not actual_city:
            return True  # If we can't determine, allow it
        
        target_lower = target_city.lower().strip()
        actual_lower = actual_city.lower().strip()
        
        # Exact match
        if target_lower == actual_lower:
            return True
        
        # Handle common variations and abbreviations
        city_variations = {
            'warszawa': ['warsaw'],
            'kraków': ['krakow'],
            'wrocław': ['wroclaw'],
            'poznań': ['poznan'],
            'gdańsk': ['gdansk'],
            'szczecin': [],
            'łódź': ['lodz'],
            'lublin': [],
            'katowice': [],
            'białystok': ['bialystok'],
            'gdynia': [],
            'czestochowa': ['częstochowa'],
            'radom': [],
            'sosnowiec': [],
            'toruń': ['torun'],
            'kielce': [],
            'rzeszów': ['rzeszow'],
            'gliwice': [],
            'zabrze': [],
            'olsztyn': [],
            'bielsko-biała': ['bielsko-biala'],
            'bytom': [],
            'zielona góra': ['zielona-gora'],
            'rybnik': [],
            'ruda śląska': ['ruda-slaska'],
            'tychy': [],
            'dąbrowa górnicza': ['dabrowa-gornicza'],
            'opole': [],
            'elbląg': ['elblag'],
            'płock': ['plock'],
            'wałbrzych': ['walbrzych'],
            'włocławek': ['wloclawek'],
            'tarnów': ['tarnow'],
            'chorzów': ['chorzow'],
            'koszalin': [],
            'kalisz': [],
            'legnica': [],
            'grudziądz': ['grudziadz'],
            'jaworzno': [],
            'słupsk': ['slupsk'],
            'jastrzębie-zdrój': ['jastrzebie-zdroj'],
            'nowy sącz': ['nowy-sacz'],
            'siedlce': [],
            'piła': ['pila'],
            'lubin': [],
            'mysłowice': ['myslowice'],
            'konin': [],
            'piotrków trybunalski': ['piotrkow-trybunalski'],
            'inowrocław': ['inowroclaw'],
            'pszczyna': [],
            'myszków': ['myszkow'],
            'koziegłowy': ['kozieglowy'],
            'czechowice-dziedzice': ['czechowice-dziedzice'],
            'żarki': ['zarki'],
            'jordanów': ['jordanow'],
            'zakopane': [],
            'skawina': [],
            'wieliczka': [],
            'oświęcim': ['oswiecim'],
            'dobczyce': []
        }
        
        # Check if target city has variations that match actual city
        if target_lower in city_variations:
            variations = city_variations[target_lower] + [target_lower]
            if any(variation == actual_lower for variation in variations):
                return True
        
        # Check if actual city has variations that match target city
        if actual_lower in city_variations:
            variations = city_variations[actual_lower] + [actual_lower]
            if any(variation == target_lower for variation in variations):
                return True
        
        # Check for partial matches (e.g., "Kraków" in "Kraków, Małopolska")
        if target_lower in actual_lower or actual_lower in target_lower:
            return True
        
        return False
