# services/ai_data_updater.py
import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import asyncio
from services.ai_service import AIKebabAnalyzer
from services.serper_service import SerperService
from services.pocketbase_db import PocketbaseService

class AIDataUpdater:
    def __init__(self, db_service: PocketbaseService, review_service: SerperService, 
                 api_key: str):
        self.db_service = db_service
        self.review_service = review_service
        self.ai_analyzer = AIKebabAnalyzer(api_key)
        
    def update_ai_analysis_for_city(self, city_name: str, limit: int = 10, skip_existing: bool = False):
        """Update AI analysis for top kebabs in a city"""
        print(f"--- Starting AI analysis for {city_name}---")
        
        if skip_existing:
            print(f"  [--skip-existing] Will skip kebabs that already have AI analysis.")
        else:
            # Only clear if we're doing a full re-run (no --skip-existing)
            self._clear_ai_scores_for_city(city_name)
        
        # Get all top kebabs in the city
        rankings = self.db_service.get_city_rankings(city_name)
        
        if skip_existing:
            # Fetch which ones already have AI analysis in DB
            all_ids = [k['google_place_id'] for k in rankings]
            existing_ai = self.db_service.get_ai_for_places(all_ids)
            existing_ids = set(existing_ai.keys())
            
            skipped_count = sum(1 for k in rankings[:limit] if k['google_place_id'] in existing_ids)
            rankings_to_process = [k for k in rankings if k['google_place_id'] not in existing_ids]
            
            print(f"  In top {limit}: {skipped_count} already analyzed (skipped), {len(rankings_to_process)} pending.")
            # Apply limit to unprocessed only
            rankings_to_process = rankings_to_process[:limit]
        else:
            rankings_to_process = rankings[:limit]
        
        if not rankings_to_process:
            print(f"  All top {limit} kebabs already have AI analysis. Nothing to do.")
            return
        
        for kebab in rankings_to_process:
            try:
                print(f"\nAnalysis for: {kebab['name']}")
                self._analyze_single_kebab(kebab)
                time.sleep(2)  # Rate limiting
            except Exception as e:
                print(f"Error analyzing {kebab['name']}: {e}")
                continue
        
        print(f"\nAI analysis complete for {city_name}")
    
    def _analyze_single_kebab(self, kebab_data: Dict):
        """Analyze a single kebab place"""
        place_id = kebab_data['google_place_id']
        
        # Fetch reviews from Serper
        reviews = self.review_service.get_place_reviews(place_id, max_reviews=20)
        
        if not reviews:
            print(f"  Warning: No reviews found for {kebab_data['name']}")
            return
        
        print(f"  - Found {len(reviews)} reviews")
        
        # Cache reviews in database
        self._cache_reviews(kebab_data, reviews)
        
        # Run AI analysis
        ai_analysis = self.ai_analyzer.analyze_reviews_batch(reviews)
        
        # Generate Creative AI Content
        ai_summary = self.ai_analyzer.generate_ai_summary(kebab_data['name'], ai_analysis)
        ai_insight = self.ai_analyzer.generate_ai_insight(kebab_data['name'], ai_analysis)
        
        # Calculate AI-adjusted score (rigorous weighted average)
        ai_adjusted_score = self._calculate_ai_adjusted_score(
            kebab_data['rank_score'],
            ai_analysis
        )
        
        # Add insight to analysis dict for storage
        ai_analysis['creative_insight'] = ai_insight
        
        # Store AI analysis in database
        self._store_ai_analysis(kebab_data, ai_analysis, ai_adjusted_score, ai_summary)
        
        print(f"  - AI Score: {ai_adjusted_score:.1f} (was {kebab_data['rank_score']:.1f})")
        print(f"  - Sentiment: {ai_analysis['sentiment_analysis']['average_sentiment']:.2f}")
        print(f"  - Authenticity: {ai_analysis['authenticity_analysis']['authenticity_score']:.1f}%")
        print(f"  - Trend: {ai_analysis['trend_analysis']['trend']}")
    
    def _cache_reviews(self, kebab_data: Dict, reviews: List[Dict]):
        """Cache reviews in database"""
        for review in reviews:
            try:
                author_hash = hash(review['author_name'])
                # Handle review_time which might be str or datetime
                raw_time = review.get('time', '')
                if isinstance(raw_time, datetime):
                    iso_time = raw_time.isoformat()
                elif isinstance(raw_time, str) and raw_time:
                    iso_time = raw_time # Assume it's already usable or ISO
                else:
                    iso_time = datetime.now().isoformat()

                self.db_service.upsert_cached_review({
                    'kebab_place': self._get_kebab_place_id(kebab_data),
                    'google_place_id': kebab_data['google_place_id'],
                    'author_name': review['author_name'][:100],
                    'author_id': str(author_hash),
                    'rating': review['rating'],
                    'review_text': review['text'][:1000],
                    'review_time': iso_time,
                    'language': review.get('language', 'pl'),
                    'is_suspicious': False,
                    'fetched_at': datetime.now().isoformat()
                })
            except Exception as e:
                print(f"    Error caching review: {e}")
                continue

    def _calculate_ai_adjusted_score(self, base_score: float, ai_analysis: Dict) -> float:
        """Calculate AI-adjusted score using rigorous weighted average.
        
        Weighting:
        - AI Sentiment: 40% (normalized to 0-100)
        - AI Authenticity: 30% (how real the reviews feel)
        - Base Rank Score: 30% (from ratings count and stars)
        """
        # 1. Sentiment Score (normalized -1..1 to 0..100)
        sentiment = ai_analysis['sentiment_analysis']['average_sentiment']
        sentiment_score = (sentiment + 1) * 50
        
        # 2. Authenticity Score (0-100)
        authenticity_score = ai_analysis['authenticity_analysis']['authenticity_score']
        
        # 3. Base Score (0-100)
        base_component = base_score
        
        # Weighted calculation
        final_score = (sentiment_score * 0.4) + (authenticity_score * 0.3) + (base_component * 0.3)
        
        # Penalties:
        # Heavily penalize places with very low authenticity
        if authenticity_score < 70:
            penalty = (70 - authenticity_score) * 1.5
            final_score -= penalty
            
        # Penalize if trend is problematic
        if ai_analysis['trend_analysis']['trend'] in ['wyraźny regres', 'niepokojący spadek']:
            final_score -= 8
            
        return float(max(0, min(100, final_score)))
    
    def _generate_summary(self, kebab_name: str, ai_analysis: Dict) -> str:
        """Generate human-readable summary"""
        sentiment = ai_analysis['sentiment_analysis']['average_sentiment']
        trend = ai_analysis['trend_analysis']['trend']
        best_aspect = ai_analysis['aspect_analysis']['best_aspect']
        satisfaction = ai_analysis['customer_insights']['customer_satisfaction_index']
        
        # Build summary parts
        parts = []
        
        # Sentiment part
        if sentiment > 0.5:
            parts.append("Klienci są bardzo zadowoleni")
        elif sentiment > 0:
            parts.append("Klienci są generalnie zadowoleni")
        elif sentiment < -0.5:
            parts.append("Klienci wyrażają niezadowolenie")
        else:
            parts.append("Opinie są mieszane")
        
        # Best aspect
        if best_aspect:
            aspect_names = {
                'meat': 'mięso',
                'sauce': 'sosy',
                'vegetables': 'warzywa',
                'service': 'obsługa',
                'portion': 'porcje',
                'price': 'ceny'
            }
            parts.append(f"szczególnie chwalą {aspect_names.get(best_aspect, best_aspect)}")
        
        # Trend
        if trend == 'improving':
            parts.append("jakość się poprawia")
        elif trend == 'declining':
            parts.append("jakość spada")
        
        # Join parts
        summary = f"{kebab_name}: {', '.join(parts)}. "
        summary += f"Wskaźnik satysfakcji: {satisfaction:.0f}%"
        
        return summary
    
    def _store_ai_analysis(self, kebab_data: Dict, ai_analysis: Dict, 
                          ai_score: float, ai_summary: str):
        """Store AI analysis in database"""
        try:
            kebab_place_id = self._get_kebab_place_id(kebab_data)
            
            # Upsert AI analysis
            self.db_service.upsert_ai_analysis(
                kebab_place_id=kebab_place_id,
                ai_analysis=ai_analysis,
                ai_score=ai_score,
                ai_summary=ai_summary
            )
            
            # Update latest rating with AI score
            self.db_service.update_rating_ai_data(
                kebab_place_id=kebab_place_id,
                ai_score=ai_score,
                ai_confidence=ai_analysis.get('ai_confidence_score', 0)
            )
            
        except Exception as e:
            print(f"Error storing AI analysis: {e}")
    
    def _clear_ai_scores_for_city(self, city_name: str):
        """Clear all AI scores for kebabs in a city"""
        try:
            city_id = self.db_service.get_city_id(city_name)
            if not city_id:
                print(f"  Error: City not found: {city_name}")
                return
            
            self.db_service.delete_ai_analysis_for_city(city_id)
            print(f"  Cleared AI scores for {city_name}")
        except Exception as e:
            print(f"  Error clearing AI scores: {e}")

    def _get_kebab_place_id(self, kebab_data: Dict) -> str:
        """Get kebab place ID from database"""
        place_id = self.db_service.get_place_id(kebab_data['google_place_id'])
        if place_id:
            return place_id
        raise ValueError(f"Kebab place not found: {kebab_data['name']}")
    
    def get_ai_insights_for_display(self, kebab_place_id: int) -> Dict:
        """Get AI insights formatted for display"""
        try:
            response = self.db_service.client.table('ai_analysis').select('*').eq(
                'kebab_place_id', kebab_place_id
            ).order('created_at', desc=True).limit(1).execute()
            
            if not response.data:
                return None
            
            analysis = response.data[0]
            data = analysis['analysis_data']
            
            # Format for frontend display
            return {
                'ai_score': round(analysis['ai_score'], 1),
                'ai_summary': analysis['ai_summary'],
                'confidence': round(analysis['confidence_score'], 1),
                'sentiment': {
                    'score': data['sentiment_analysis']['average_sentiment'],
                    'label': self._get_sentiment_label(data['sentiment_analysis']['average_sentiment']),
                    'distribution': data['sentiment_analysis']['sentiment_distribution']
                },
                'authenticity': {
                    'score': data['authenticity_analysis']['authenticity_score'],
                    'suspicious_count': data['authenticity_analysis']['suspicious_count']
                },
                'trends': {
                    'direction': data['trend_analysis']['trend'],
                    'momentum': data['trend_analysis']['momentum']
                },
                'best_features': data['aspect_analysis']['best_aspect'],
                'worst_features': data['aspect_analysis']['worst_aspect'],
                'customer_type': data['customer_insights']['primary_customer_type'],
                'satisfaction_index': data['customer_insights']['customer_satisfaction_index'],
                'last_updated': analysis['updated_at']
            }
        except Exception as e:
            print(f"Error getting AI insights: {e}")
            return None
    
    def _get_sentiment_label(self, score: float) -> str:
        """Convert sentiment score to label with more variety"""
        if score > 0.6:
            return 'absolutny zachwyt'
        elif score > 0.3:
            return 'bardzo pozytywne'
        elif score > 0.1:
            return 'lekki entuzjazm'
        elif score < -0.6:
            return 'miażdżąca krytyka'
        elif score < -0.3:
            return 'wyraźna niechęć'
        elif score < -0.1:
            return 'lekkie rozczarowanie'
        else:
            return 'mieszane odczucia'
