# services/ranking.py
from typing import List, Dict

class RankingService:
    def calculate_rank_score(self, rating: float, total_reviews: int, positive_percentage: float = 0) -> float:
        """
        Calculate ranking score based on:
        - Primary factor: Star rating (weight: 85%)
        - Secondary factor: Review count reliability (weight: 15%)
        
        Note: Positive percentage is ignored as it's not real data
        """
        # Normalize rating (0-5 stars to 0-100) with high weight
        rating_score = (rating / 5) * 100 * 0.85
        
        # Review count reliability score (logarithmic scale)
        # More reviews = more reliable rating
        import math
        # Cap at 1000 reviews for calculation
        review_reliability = min(math.log10(min(total_reviews, 1000) + 1) / 3 * 100, 100) * 0.15
        
        # Total score
        total_score = rating_score + review_reliability
        
        return round(total_score, 2)
    
    def rank_kebabs(self, kebabs: List[Dict], previous_rankings: List[Dict] = None) -> List[Dict]:
        """
        Rank kebabs based on calculated scores and track changes from previous rankings
        """
        # Calculate scores for each kebab
        for kebab in kebabs:
            kebab['rank_score'] = self.calculate_rank_score(
                kebab.get('rating', 0),
                kebab.get('total_reviews', 0),
                kebab.get('positive_percentage', 0)
            )
        
        # Sort by rank score (descending), then by total_reviews (descending) for tiebreaker
        ranked_kebabs = sorted(kebabs, 
                             key=lambda x: (x['rank_score'], x.get('total_reviews', 0)), 
                             reverse=True)
        
        # Add rank positions and track changes
        previous_ranks = {}
        if previous_rankings:
            for k in previous_rankings:
                # Handle both field name variations for compatibility
                place_id = k.get('google_place_id') or k.get('place_id')
                if place_id and 'city_rank' in k:
                    previous_ranks[place_id] = k['city_rank']
        
        for i, kebab in enumerate(ranked_kebabs):
            kebab['city_rank'] = i + 1
            
            # Get place_id using both possible field names for compatibility
            place_id = kebab.get('google_place_id') or kebab.get('place_id')
            
            if not place_id:
                print(f"Warning: Kebab '{kebab.get('name', 'Unknown')}' missing place_id")
                continue
            
            # Calculate rank change if previous ranking exists
            if place_id in previous_ranks:
                previous_rank = previous_ranks[place_id]
                kebab['rank_change'] = previous_rank - (i + 1)  # Positive = improved
            else:
                # New entry in rankings
                kebab['is_new'] = True
        
        return ranked_kebabs
    
    def filter_quality_kebabs(self, kebabs: List[Dict]) -> List[Dict]:
        """
        Filter out low-quality entries
        """
        min_reviews = 10  # Minimum reviews to be considered
        min_rating = 3.0  # Minimum rating to be included
        
        return [
            kebab for kebab in kebabs
            if kebab.get('total_reviews', 0) >= min_reviews
            and kebab.get('rating', 0) >= min_rating
        ]
