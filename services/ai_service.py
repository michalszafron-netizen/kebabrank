# services/ai_service.py
import os
import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from collections import Counter
import openai
from textblob import TextBlob
from statistics import mean, stdev

class AIKebabAnalyzer:
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        # DeepSeek is OpenAI-compatible
        import openai
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        self.model = model
        
        # Polish sentiment words for quick analysis
        self.polish_positive = ['pyszny', 'świetny', 'super', 'polecam', 'najlepszy', 
                               'smaczny', 'świeży', 'dobry', 'rewelacyjny', 'mistrz']
        self.polish_negative = ['okropny', 'zimny', 'stary', 'brzydki', 'drogi', 
                               'mały', 'słaby', 'kiepski', 'fatalny', 'najgorszy']
        
        # Aspect keywords
        self.aspects = {
            'meat': ['mięso', 'kurczak', 'wołowina', 'baranina', 'meat', 'chicken'],
            'sauce': ['sos', 'ostry', 'łagodny', 'czosnkowy', 'sauce', 'spicy'],
            'vegetables': ['warzywa', 'sałata', 'pomidor', 'ogórek', 'vegetables'],
            'service': ['obsługa', 'miły', 'szybko', 'czekać', 'service', 'fast'],
            'portion': ['duży', 'mały', 'porcja', 'wielkość', 'size', 'portion'],
            'price': ['cena', 'drogo', 'tanio', 'złotych', 'price', 'expensive']
        }
    
    def analyze_reviews_batch(self, reviews: List[Dict]) -> Dict:
        """Analyze a batch of reviews for a kebab place"""
        if not reviews:
            return self._empty_analysis()
        
        analysis = {
            'sentiment_analysis': self._analyze_sentiments(reviews),
            'authenticity_analysis': self._detect_fake_reviews(reviews),
            'trend_analysis': self._analyze_trends(reviews),
            'aspect_analysis': self._analyze_aspects(reviews),
            'customer_insights': self._analyze_customers(reviews),
            'ai_confidence_score': 0.0,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Calculate overall AI confidence
        analysis['ai_confidence_score'] = self._calculate_confidence(analysis, len(reviews))
        
        return analysis
    
    def _analyze_sentiments(self, reviews: List[Dict]) -> Dict:
        """Analyze sentiment of reviews"""
        sentiments = []
        emotions = []
        
        for review in reviews:
            text = review.get('text', '').lower()
            rating = review.get('rating', 3)
            
            # Quick sentiment based on rating
            if rating >= 4:
                base_sentiment = 0.7
            elif rating >= 3:
                base_sentiment = 0.0
            else:
                base_sentiment = -0.7
            
            # Refine with text analysis
            text_sentiment = self._analyze_text_sentiment(text)
            combined_sentiment = (base_sentiment * 0.6) + (text_sentiment * 0.4)
            
            sentiments.append(combined_sentiment)
            emotions.append(self._detect_emotion(text))
        
        # Aggregate results
        avg_sentiment = mean(sentiments) if sentiments else 0
        
        return {
            'average_sentiment': round(avg_sentiment, 2),
            'sentiment_distribution': {
                'positive': len([s for s in sentiments if s > 0.3]),
                'neutral': len([s for s in sentiments if -0.3 <= s <= 0.3]),
                'negative': len([s for s in sentiments if s < -0.3])
            },
            'dominant_emotions': Counter(emotions).most_common(3),
            'sentiment_trend': self._calculate_sentiment_trend(reviews)
        }
    
    def _analyze_text_sentiment(self, text: str) -> float:
        """Analyze sentiment of text"""
        if not text:
            return 0.0
        
        # Count positive and negative words
        positive_count = sum(1 for word in self.polish_positive if word in text)
        negative_count = sum(1 for word in self.polish_negative if word in text)
        
        # Use TextBlob for English text
        try:
            blob = TextBlob(text)
            english_sentiment = blob.sentiment.polarity
        except:
            english_sentiment = 0
        
        # Combine Polish and English analysis
        polish_sentiment = (positive_count - negative_count) * 0.3
        combined = (polish_sentiment + english_sentiment) / 2
        
        return max(-1, min(1, combined))  # Clamp to [-1, 1]
    
    def _detect_emotion(self, text: str) -> str:
        """Detect primary emotion in text with more Polish flavor"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['love', 'kocham', 'najlepszy', 'rewelacja', 'sztos', 'petarda', 'mistrzostwo']):
            return 'zachwyt'
        elif any(word in text_lower for word in ['happy', 'zadowolony', 'super', ':)', 'smaczne', 'polecam']):
            return 'zadowolenie'
        elif any(word in text_lower for word in ['angry', 'wściekły', 'skandal', '!!', 'tragedia', 'dramat', 'fuj']):
            return 'gniew'
        elif any(word in text_lower for word in ['disappointed', 'rozczarowany', 'szkoda', 'słabo', 'średnio', 'bez szału']):
            return 'rozczarowanie'
        elif any(word in text_lower for word in ['zimne', 'surowe', 'stare', 'brudno']):
            return 'irytacja'
        else:
            return 'neutralność'
    
    def _detect_fake_reviews(self, reviews: List[Dict]) -> Dict:
        """Detect potential fake reviews"""
        suspicious_patterns = []
        
        # Check for common fake review patterns
        for i, review in enumerate(reviews):
            suspicion_score = 0
            reasons = []
            
            text = review.get('text', '')
            author = review.get('author_name', '')
            date = review.get('time', datetime.now())
            
            # Pattern 1: Very short generic reviews
            if len(text) < 20 and review.get('rating') == 5:
                suspicion_score += 0.3
                reasons.append('generic_short')
            
            # Pattern 2: No specific details
            if not any(aspect in text.lower() for aspects in self.aspects.values() for aspect in aspects):
                suspicion_score += 0.2
                reasons.append('no_specifics')
            
            # Pattern 3: Multiple reviews from same author
            author_reviews = [r for r in reviews if r.get('author_name') == author]
            if len(author_reviews) > 1:
                suspicion_score += 0.3
                reasons.append('multiple_reviews')
            
            # Pattern 4: Review bombing (many reviews in short time)
            # Need to handle potential datetime/str
            try:
                rev_time = date if isinstance(date, datetime) else datetime.fromisoformat(str(date).replace('Z', '+00:00'))
                same_day_reviews = [r for r in reviews if 
                                abs((r.get('time', rev_time) - rev_time).days) < 1]
                if len(same_day_reviews) > 5:
                    suspicion_score += 0.2
                    reasons.append('review_bombing')
            except: pass
            
            if suspicion_score > 0.5:
                suspicious_patterns.append({
                    'review_index': i,
                    'suspicion_score': suspicion_score,
                    'reasons': reasons
                })
        
        # Calculate overall authenticity
        total_suspicious = len(suspicious_patterns)
        authenticity_score = max(0, 100 - (total_suspicious / len(reviews) * 100 if reviews else 0))
        
        return {
            'authenticity_score': round(authenticity_score, 1),
            'suspicious_count': total_suspicious,
            'suspicious_patterns': suspicious_patterns[:5],  # Top 5 most suspicious
            'review_velocity': self._calculate_review_velocity(reviews)
        }
    
    def _analyze_trends(self, reviews: List[Dict]) -> Dict:
        """Analyze rating and sentiment trends over time"""
        if len(reviews) < 5:
            return {'trend': 'insufficient_data', 'momentum': 0}
        
        # Sort reviews by time
        sorted_reviews = sorted(reviews, key=lambda x: x.get('time', datetime.now()))
        
        # Split into old and new halves
        mid_point = len(sorted_reviews) // 2
        old_reviews = sorted_reviews[:mid_point]
        new_reviews = sorted_reviews[mid_point:]
        
        # Calculate average ratings
        old_avg = mean([r.get('rating', 3) for r in old_reviews])
        new_avg = mean([r.get('rating', 3) for r in new_reviews])
        
        # Calculate trend with more granularity
        rating_change = new_avg - old_avg
        
        if rating_change > 0.6:
            trend = 'dynamiczny wzrost'
            momentum = min(100, rating_change * 50)
        elif rating_change > 0.15:
            trend = 'lekka poprawa'
            momentum = rating_change * 40
        elif rating_change < -0.6:
            trend = 'wyraźny regres'
            momentum = max(-100, rating_change * 50)
        elif rating_change < -0.15:
            trend = 'niepokojący spadek'
            momentum = rating_change * 40
        else:
            trend = 'pełna stabilizacja'
            momentum = 0
        
        return {
            'trend': trend,
            'momentum': round(momentum, 1),
            'old_average': round(old_avg, 2),
            'new_average': round(new_avg, 2),
            'volatility': self._calculate_volatility(sorted_reviews)
        }
    
    def _analyze_aspects(self, reviews: List[Dict]) -> Dict:
        """Analyze specific aspects mentioned in reviews"""
        aspect_sentiments = {aspect: [] for aspect in self.aspects}
        aspect_mentions = {aspect: 0 for aspect in self.aspects}
        
        for review in reviews:
            text = review.get('text', '').lower()
            review_sentiment = self._analyze_text_sentiment(text)
            
            for aspect, keywords in self.aspects.items():
                if any(keyword in text for keyword in keywords):
                    aspect_mentions[aspect] += 1
                    aspect_sentiments[aspect].append(review_sentiment)
        
        # Calculate average sentiment per aspect
        aspect_scores = {}
        for aspect, sentiments in aspect_sentiments.items():
            if sentiments:
                aspect_scores[aspect] = {
                    'score': round(mean(sentiments), 2),
                    'mentions': aspect_mentions[aspect],
                    'percentage': round(aspect_mentions[aspect] / len(reviews) * 100, 1) if reviews else 0
                }
        
        # Find best and worst aspects
        if aspect_scores:
            best_aspect = max(aspect_scores.items(), 
                            key=lambda x: x[1]['score'] if x[1]['mentions'] > 2 else -999)
            worst_aspect = min(aspect_scores.items(), 
                             key=lambda x: x[1]['score'] if x[1]['mentions'] > 2 else 999)
        else:
            best_aspect = worst_aspect = None
        
        return {
            'aspect_scores': aspect_scores,
            'best_aspect': best_aspect[0] if best_aspect else None,
            'worst_aspect': worst_aspect[0] if worst_aspect else None,
            'top_keywords': self._extract_keywords(reviews)
        }
    
    def _analyze_customers(self, reviews: List[Dict]) -> Dict:
        """Analyze customer patterns and demographics"""
        visit_times = []
        author_types = []
        
        for review in reviews:
            # Estimate visit time from review text
            text = review.get('text', '').lower()
            
            if any(word in text for word in ['lunch', 'obiad', 'w południe']):
                visit_times.append('lunch')
            elif any(word in text for word in ['dinner', 'kolacja', 'wieczorem']):
                visit_times.append('dinner')
            elif any(word in text for word in ['late', 'nocą', 'po imprezie']):
                visit_times.append('late_night')
            
            # Estimate customer type
            if any(word in text for word in ['student', 'studia', 'akademik']):
                author_types.append('student')
            elif any(word in text for word in ['family', 'rodzina', 'dzieci']):
                author_types.append('family')
            elif any(word in text for word in ['work', 'praca', 'biuro']):
                author_types.append('professional')
        
        return {
            'primary_customer_type': Counter(author_types).most_common(1)[0][0] if author_types else 'smakosze uliczni',
            'peak_times': Counter(visit_times).most_common(2),
            'loyalty_indicator': self._calculate_loyalty(reviews),
            'customer_satisfaction_index': self._calculate_satisfaction_index(reviews)
        }
    
    def _calculate_confidence(self, analysis: Dict, review_count: int) -> float:
        """Calculate confidence in AI analysis"""
        confidence = 50.0  # Base confidence
        
        # More reviews = higher confidence
        confidence += min(30, review_count * 0.3)
        
        # Consistent patterns = higher confidence
        if analysis['sentiment_analysis']['average_sentiment'] != 0:
            confidence += 10
        
        # Authenticity affects confidence
        confidence *= (analysis['authenticity_analysis']['authenticity_score'] / 100)
        
        return round(min(95, confidence), 1)
    
    def _calculate_sentiment_trend(self, reviews: List[Dict]) -> str:
        """Calculate if sentiment is improving or declining"""
        if len(reviews) < 10:
            return 'stable'
        
        # Get sentiments over time
        time_sentiments = []
        for review in sorted(reviews, key=lambda x: x.get('time', datetime.now())):
            sentiment = self._analyze_text_sentiment(review.get('text', ''))
            time_sentiments.append(sentiment)
        
        # Compare first third with last third
        third = len(time_sentiments) // 3
        early_avg = mean(time_sentiments[:third])
        late_avg = mean(time_sentiments[-third:])
        
        diff = late_avg - early_avg
        if diff > 0.2:
            return 'improving'
        elif diff < -0.2:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_review_velocity(self, reviews: List[Dict]) -> Dict:
        """Calculate review posting velocity"""
        if len(reviews) < 2:
            return {'velocity': 'normal', 'reviews_per_month': 0}
        
        # Sort by time
        sorted_reviews = sorted(reviews, key=lambda x: x.get('time', datetime.now()))
        
        # Calculate time span
        first_review = sorted_reviews[0].get('time', datetime.now())
        last_review = sorted_reviews[-1].get('time', datetime.now())
        months_span = max(1, (last_review - first_review).days / 30)
        
        reviews_per_month = len(reviews) / months_span
        
        if reviews_per_month > 50:
            velocity = 'suspicious'
        elif reviews_per_month > 20:
            velocity = 'high'
        elif reviews_per_month < 2:
            velocity = 'low'
        else:
            velocity = 'normal'
        
        return {
            'velocity': velocity,
            'reviews_per_month': round(reviews_per_month, 1)
        }
    
    def _calculate_volatility(self, reviews: List[Dict]) -> float:
        """Calculate rating volatility"""
        if len(reviews) < 3:
            return 0.0
        
        ratings = [r.get('rating', 3) for r in reviews]
        return round(stdev(ratings), 2)
    
    def _extract_keywords(self, reviews: List[Dict]) -> List[str]:
        """Extract most common keywords from reviews"""
        all_words = []
        stop_words = {'i', 'w', 'z', 'że', 'to', 'jest', 'na', 'się', 'nie', 
                     'the', 'is', 'at', 'it', 'and', 'or', 'but'}
        
        for review in reviews:
            text = review.get('text', '').lower()
            words = re.findall(r'\b\w+\b', text)
            words = [w for w in words if len(w) > 3 and w not in stop_words]
            all_words.extend(words)
        
        return [word for word, _ in Counter(all_words).most_common(10)]
    
    def _calculate_loyalty(self, reviews: List[Dict]) -> str:
        """Estimate customer loyalty based on review patterns"""
        # Look for returning customers
        authors = [r.get('author_name', '') for r in reviews]
        unique_authors = len(set(authors))
        total_reviews = len(reviews)
        
        if total_reviews == 0:
            return 'unknown'
        
        repeat_ratio = 1 - (unique_authors / total_reviews)
        
        if repeat_ratio > 0.3:
            return 'high'
        elif repeat_ratio > 0.1:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_satisfaction_index(self, reviews: List[Dict]) -> float:
        """Calculate overall customer satisfaction index (0-100)"""
        if not reviews:
            return 50.0
        
        # Combine multiple factors
        avg_rating = mean([r.get('rating', 3) for r in reviews])
        sentiment_score = mean([self._analyze_text_sentiment(r.get('text', '')) 
                               for r in reviews])
        
        # Convert to 0-100 scale
        rating_component = (avg_rating / 5) * 50
        sentiment_component = ((sentiment_score + 1) / 2) * 50
        
        return round(rating_component + sentiment_component, 1)
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure"""
        return {
            'sentiment_analysis': {
                'average_sentiment': 0,
                'sentiment_distribution': {'positive': 0, 'neutral': 0, 'negative': 0},
                'dominant_emotions': [],
                'sentiment_trend': 'insufficient_data'
            },
            'authenticity_analysis': {
                'authenticity_score': 100,
                'suspicious_count': 0,
                'suspicious_patterns': [],
                'review_velocity': {'velocity': 'normal', 'reviews_per_month': 0}
            },
            'trend_analysis': {
                'trend': 'insufficient_data',
                'momentum': 0,
                'volatility': 0
            },
            'aspect_analysis': {
                'aspect_scores': {},
                'best_aspect': None,
                'worst_aspect': None,
                'top_keywords': []
            },
            'customer_insights': {
                'primary_customer_type': 'unknown',
                'peak_times': [],
                'loyalty_indicator': 'unknown',
                'customer_satisfaction_index': 50.0
            },
            'ai_confidence_score': 0.0,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def generate_ai_summary(self, kebab_name: str, analysis: Dict) -> str:
        """Generate human-readable AI summary using DeepSeek"""
        try:
            prompt = f"""
            Na podstawie poniższej analizy kebabowni "{kebab_name}", Napisz zwięzły, ale soczysty opis. Niech każde słowo ma znaczenie po polsku.
            Opisz atmosferę miejsca i konkretne smaki, które je wyróżniają. 
            Używaj BOGATEGO, EKSPERCKIEGO języka. Używaj nieszablonowych przymiotników i unikaj frazesów.
            
            UŻYWAJ WYŁĄCZNIE JĘZYKA POLSKIEGO. Żadnych angielskich wstawek.

            Sentyment (1.0 to max): {analysis['sentiment_analysis']['average_sentiment']}
            Główny atut: {analysis['aspect_analysis']['best_aspect']}
            Najgorszy atut: {analysis['aspect_analysis']['worst_aspect']}
            Atmosfera/Typ klienta: {analysis['customer_insights']['primary_customer_type']}
            Trend: {analysis['trend_analysis']['trend']}
            Weryfikacja autentyczności (0-100): {analysis['authenticity_analysis']['authenticity_score']}%
            
            Zwróć TYLKO opis.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Jesteś polskim ekspertem kulinarnym, krytykiem, który kocha street-food, ale ma wysokie wymagania. Piszesz barwnie, opisowo i wyłącznie po polsku."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip().strip('"')
        except Exception as e:
            print(f"DeepSeek Summary Error: {e}")
            return "Solidny wybór z ciekawym akcentem smakowym."

    def generate_ai_insight(self, kebab_name: str, analysis: Dict) -> str:
        """Generate a unique "Expert Tip" or insight for this place"""
        try:
            prompt = f"""
            Podaj jedną unikalną radę lub spostrzeżenie (tzw. 'Expert Tip') dla miejsca "{kebab_name}" po polsku.
            Bazuj na tych danych:
            Wady: {analysis['aspect_analysis']['worst_aspect']}
            Zalety: {analysis['aspect_analysis']['best_aspect']}
            Typ klienta: {analysis['customer_insights']['primary_customer_type']}
            Klimat: {analysis['trend_analysis']['trend']}
            
            Przykład: 'Bierz baraninę, ale omijaj sos łagodny - jest mdły.' lub 'Najlepiej wpadać po 22:00, mniejszy tłok.'
            Zwróć TYLKO radę (max 15 słów).
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Jesteś warszawskim znawcą kebabów (kebab-master), znasz każdy trick."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.9
            )
            
            return response.choices[0].message.content.strip().strip('"')
        except Exception as e:
            print(f"DeepSeek Insight Error: {e}")
            return "Warto spróbować autorskiego sosu."