# app.py - Main Flask application
from flask import Flask, jsonify, render_template, request, send_from_directory, redirect
from flask_cors import CORS
from flask_caching import Cache
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import threading
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Response

from services.google_places import GooglePlacesService
from services.pocketbase_db import PocketbaseService
from services.ranking import RankingService
from services.city_grammar import locative
from services.data_updater import DataUpdater
# --- START: Add AI-related imports ---
from services.ai_data_updater import AIDataUpdater
# Assuming GooglePlacesEnhancedService is a new service you created
from services.google_places_enhanced import GooglePlacesEnhancedService
# --- END: Add AI-related imports ---


load_dotenv()

app = Flask(__name__)
CORS(app)

# Enable gzip compression for all text responses
from flask_compress import Compress
app.config['COMPRESS_MIMETYPES'] = [
    'text/html', 'text/css', 'application/javascript',
    'application/json', 'text/plain'
]
app.config['COMPRESS_LEVEL'] = 6
app.config['COMPRESS_MIN_SIZE'] = 500
Compress(app)

# Configure caching
cache_config = {
    'CACHE_TYPE': 'SimpleCache',  # In-memory cache for development
    'CACHE_DEFAULT_TIMEOUT': 300,  # 5 minutes default
    'CACHE_THRESHOLD': 1000  # Maximum number of items to cache
}
app.config.from_mapping(cache_config)
cache = Cache(app)

# Initialize services
google_service = GooglePlacesService(os.getenv('GOOGLE_API_KEY'))
db_service = PocketbaseService(
    os.getenv('PB_URL'), 
    os.getenv('PB_EMAIL'), 
    os.getenv('PB_PASSWORD')
)
ranking_service = RankingService()
data_updater = DataUpdater(google_service, db_service, ranking_service)


def translate_ai_summary(summary: str, target_lang: str) -> str:
    """Simple translation function for AI summaries"""
    if target_lang == 'en' and summary:
        # Basic Polish to English translations
        translations = {
            'Klienci są bardzo zadowoleni': 'Customers are very satisfied',
            'Klienci są generalnie zadowoleni': 'Customers are generally satisfied',
            'Klienci wyrażają niezadowolenie': 'Customers express dissatisfaction',
            'Opinie są mieszane': 'Reviews are mixed',
            'szczególnie chwalą': 'especially praise',
            'mięso': 'meat',
            'sosy': 'sauces',
            'warzywa': 'vegetables',
            'obsługa': 'service',
            'porcje': 'portions',
            'ceny': 'prices',
            'jakość się poprawia': 'quality is improving',
            'jakość spada': 'quality is declining',
            'Wskaźnik satysfakcji': 'Satisfaction index'
        }
        
        # Apply translations
        result = summary
        for pl, en in translations.items():
            result = result.replace(pl, en)
        
        return result
    
    return summary

@app.after_request
def add_header(response):
    """Add headers to both force latest IE rendering engine or to cache static assets"""
    if request.path.startswith('/static/'):
        # Cache static assets for 30 days
        response.cache_control.max_age = 2592000
    return response

@app.before_request
def redirect_to_www():
    """Redirect non-www to www for better SEO"""
    urlparts = request.url_root.split('://')
    if len(urlparts) > 1:
        scheme = urlparts[0]
        host = urlparts[1].split(':')[0] # Remove port if present
        
        # Only redirect on production domain and if not already www
        if host == 'kebabrank.com':
            return redirect(f"{scheme}://www.{host}{request.full_path}", code=301)

@app.context_processor
def inject_cities():
    """Make cities available to all templates for the Mega Menu"""
    cached = cache.get('inject_cities_result')
    if cached:
        return cached

    all_cities = db_service.get_cities()

    # Sort A-Z
    all_cities.sort(key=lambda x: x.get('name', ''))
    
    # Define popular cities for the top section
    popular_names = ["Warszawa", "Kraków", "Wrocław", "Gdańsk", "Poznań", "Łódź"]
    popular_cities = [c for c in all_cities if c['name'] in popular_names]
    # Sort popular cities in the order of the list above
    popular_cities.sort(key=lambda x: popular_names.index(x['name']) if x['name'] in popular_names else 99)
    
    # Pre-calculate slugs for consistency
    def slugify(text):
        import urllib.parse
        polish_mapping = {'ł': 'l', 'ó': 'o', 'ą': 'a', 'ę': 'e', 'ć': 'c', 'ń': 'n', 'ś': 's', 'ź': 'z', 'ż': 'z'}
        text = text.lower()
        for char, repl in polish_mapping.items():
            text = text.replace(char, repl)
        return text.replace(' ', '-')

    for city in all_cities:
        city['slug'] = slugify(city['name'])
    for city in popular_cities:
        city['slug'] = slugify(city['name'])
        
    result = dict(available_cities=all_cities, popular_cities=popular_cities)
    if all_cities:  # Don't cache empty result — may be a transient PocketBase error
        cache.set('inject_cities_result', result, timeout=3600)
    return result

@app.route('/')
def index():
    """Main page"""
    seo_rankings = cache.get('index_seo_rankings')
    if seo_rankings is None:
        seo_rankings = db_service.get_global_rankings(limit=5)
        cache.set('index_seo_rankings', seo_rankings, timeout=3600)
    
    return render_template('index.html',
                         initial_city='Kraków',
                         page_title="Kebab Rank 2026 - Ranking Najlepszych Kebabów w Polsce | Wspierany AI",
                         page_description="Odkryj najlepsze kebaby w Polsce! Kebab Rank 2026 to pierwszy w kraju ranking kebabów wspierany przez sztuczną inteligencję. Znajdź swój ulubiony lokal!",
                         page_keywords="kebab, ranking kebabów, najlepszy kebab w Polsce, doner, tortilla, kebab ranking, jedzenie, rzemieślniczy kebab",
                         seo_rankings=seo_rankings,
                         seo_city_locative="Polsce")


def _city_seo_meta(city_name):
    """
    Buduje meta-tagi strony miasta z poprawną odmianą przez miejscownik.
    Wcześniej dawało to niegramatyczne "Najlepszy kebab w Kraków" na 71 stronach.
    Keywords celowo mieszają mianownik i miejscownik — ludzie szukają obu form.
    """
    loc = locative(city_name)
    return {
        'page_title': f"Najlepszy kebab w {loc} – Ranking kebabów 2026 | KebabRank",
        'page_description': (
            f"Ranking najlepszych kebabów w {loc}. Sprawdź, gdzie zjeść najlepszy "
            f"doner i tortillę w {loc} — na podstawie ocen Google i analizy AI."
        ),
        'page_keywords': (
            f"kebab {city_name}, najlepszy kebab w {loc}, kebaby {city_name}, "
            f"doner {city_name}, tortilla {city_name}, ranking kebabów {city_name}"
        ),
        'page_h1': f"Najlepszy kebab w {loc}",
        'seo_city_locative': loc,
    }


@app.route('/kebab-<city_slug>')
def city_page_seo(city_slug):
    """SEO-optimized city URLs with 'kebab-' prefix"""
    try:
        cities = db_service.get_cities()
        city_mapping = {}
        import urllib.parse
        decoded_slug = urllib.parse.unquote(city_slug)
        
        for city in cities:
            city_name = city['name']
            basic_slug = city_name.lower().replace(' ', '-')
            city_mapping[basic_slug] = city_name
            
            polish_mapping = {'ł': 'l', 'ó': 'o', 'ą': 'a', 'ę': 'e', 'ć': 'c', 'ń': 'n', 'ś': 's', 'ź': 'z', 'ż': 'z'}
            polish_slug = city_name.lower()
            for char, repl in polish_mapping.items(): polish_slug = polish_slug.replace(char, repl)
            polish_slug = polish_slug.replace(' ', '-')
            city_mapping[polish_slug] = city_name
            city_mapping[city_name.lower()] = city_name
        
        search_slug = decoded_slug.lower()
        if search_slug in city_mapping:
            city_name = city_mapping[search_slug]
            # Fetch city rankings for SEO
            city_rankings = db_service.get_city_rankings(city_name, limit=10)
            return render_template('index.html', initial_city=city_name,
                                 seo_rankings=city_rankings,
                                 **_city_seo_meta(city_name))
        else:
            # Try to find a close match
            for slug, name in city_mapping.items():
                if search_slug in slug or slug in search_slug:
                    city_name = name
                    city_rankings = db_service.get_city_rankings(city_name, limit=10)
                    return render_template('index.html',
                                         initial_city=city_name,
                                         seo_rankings=city_rankings,
                                         **_city_seo_meta(city_name))

            return render_template('blog/404.html'), 404
    except Exception as e:
        print(f"Error in city_page_seo route: {e}")
        return render_template('blog/404.html'), 404

@app.route('/privacy')
@cache.cached(timeout=3600)
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html', current_date=datetime.now().strftime('%d.%m.%Y'))

@app.route('/terms')
@cache.cached(timeout=3600)
def terms():
    """Terms of Service page"""
    return render_template('terms.html', current_date=datetime.now().strftime('%d.%m.%Y'))

@app.route('/<city_slug>')
def city_page_redirect(city_slug):
    """301 Redirect from old city URLs to new SEO-optimized URLs"""
    try:
        cities = db_service.get_cities()
        # Create mapping of slugified city names to actual city names
        city_mapping = {}
        
        # Handle URL-encoded Polish characters properly
        import urllib.parse
        decoded_slug = urllib.parse.unquote(city_slug)
        
        for city in cities:
            # Create multiple slug variations for better matching
            city_name = city['name']
            
            # Basic slug (spaces to hyphens, lowercase)
            basic_slug = city_name.lower().replace(' ', '-')
            city_mapping[basic_slug] = city_name
            
            # Handle Polish characters properly
            polish_mapping = {
                'ł': 'l', 'ó': 'o', 'ą': 'a', 'ę': 'e', 'ć': 'c', 
                'ń': 'n', 'ś': 's', 'ź': 'z', 'ż': 'z'
            }
            
            # Create slug with Polish characters replaced
            polish_slug = city_name.lower()
            for polish_char, replacement in polish_mapping.items():
                polish_slug = polish_slug.replace(polish_char, replacement)
            polish_slug = polish_slug.replace(' ', '-')
            city_mapping[polish_slug] = city_name
            
            # Also handle direct city names (without slugification)
            city_mapping[city_name.lower()] = city_name
        
        # Try to match the decoded slug
        search_slug = decoded_slug.lower()
        if search_slug in city_mapping:
            # 301 Redirect to new SEO-optimized URL
            return redirect(f'/kebab-{search_slug}', code=301)
        else:
            # Try to find a close match
            for slug, name in city_mapping.items():
                if search_slug in slug or slug in search_slug:
                    # 301 Redirect to new SEO-optimized URL
                    return redirect(f'/kebab-{slug}', code=301)
            
            return render_template('blog/404.html'), 404
    except Exception as e:
        print(f"Error in city_page_redirect route: {e}")
        # Return 404 instead of redirecting to home page
        return render_template('blog/404.html'), 404


@app.route('/api/rankings/<city>')
@cache.cached(timeout=300, query_string=True)  # Cache for 5 minutes
def get_city_rankings(city):
    """Get kebab rankings for a specific city"""
    import time
    start_time = time.time()
    
    try:
        # Performance logging
        print(f"\n=== DEBUG: Starting rankings request for {city} ===")
        
        last_update = db_service.get_last_update_time(city)
        update_interval_days = int(os.getenv('DATABASE_UPDATE_INTERVAL_DAYS', 7))
        limit = min(int(request.args.get('limit', 10)), 200)  # Max 200 items
        offset = int(request.args.get('offset', 0))
        
        print(f"DEBUG: Last update: {last_update}, Interval: {update_interval_days} days")
        
        # Auto-updates disabled per user request
        print(f"DEBUG: Auto-update disabled manually. Relying on existing DB info.")
        
        # Get optimized rankings with rank change data
        db_start = time.time()
        rankings = db_service.get_city_rankings(city, limit, offset)
        db_time = time.time() - db_start
        print(f"DEBUG: Database query took {db_time:.3f}s, found {len(rankings)} rankings")
        
        response = jsonify({
            'status': 'success',
            'data': rankings,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'total': len(rankings)
            },
            'performance': {
                'db_query_time': db_time,
                'total_time': time.time() - start_time
            }
        })
        # Cache for 5 minutes since rankings don't change frequently
        response.headers['Cache-Control'] = 'public, max-age=300'
        response.headers['Vary'] = 'Accept-Encoding'
        
        total_time = time.time() - start_time
        print(f"DEBUG: Total request time: {total_time:.3f}s")
        
        return response
    except Exception as e:
        print(f"ERROR in rankings endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/rankings/global')
@cache.cached(timeout=300, query_string=True)
def get_global_rankings():
    """Get global kebab rankings with AI data"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        # Get base rankings
        rankings = db_service.get_global_rankings(limit=limit)
        
        # Enrich with AI data using bulk fetch
        google_ids = [k['google_place_id'] for k in rankings]
        ai_data_map = db_service.get_ai_for_places(google_ids)
        
        for kebab in rankings:
            ai_data = ai_data_map.get(kebab['google_place_id'])
            if ai_data:
                kebab['has_ai_analysis'] = True
                kebab['ai_score'] = ai_data.get('ai_score')
                kebab['ai_summary'] = ai_data.get('ai_summary', '')
                
                analysis_data = ai_data.get('analysis_data', {})
                kebab['ai_insights'] = {
                    'sentiment': analysis_data.get('sentiment_analysis', {}).get('score', 0),
                    'trend': analysis_data.get('trend_analysis', {}).get('trend', 'stable'),
                    'authenticity': analysis_data.get('authenticity_analysis', {}).get('authenticity_score', 100)
                }
            else:
                kebab['has_ai_analysis'] = False
                kebab['ai_score'] = kebab.get('rank_score')
                 
        return jsonify({'status': 'success', 'data': rankings})
    except Exception as e:
        print(f"Error in global rankings: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/stats')
@cache.cached(timeout=86400)
def get_stats():
    """Total kebab places and cities in the database."""
    try:
        places = db_service.client.collection('kebab_places').get_list(1, 1)
        cities = db_service.client.collection('cities').get_list(1, 1)
        return jsonify({
            'status': 'success',
            'total_places': places.total_items,
            'total_cities': cities.total_items,
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/cities')
@cache.cached(timeout=3600, query_string=True)  # Cache for 1 hour
def get_cities():
    """Get list of available cities"""
    try:
        cities = db_service.get_cities()
        response = jsonify({'status': 'success', 'data': cities})
        # Add cache headers for client-side caching
        response.headers['Cache-Control'] = 'public, max-age=3600'
        response.headers['Vary'] = 'Accept-Encoding'
        return response
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/cities/coords')
@cache.cached(timeout=86400)
def get_cities_coords():
    """Return all cities with average lat/lng computed from their kebab places."""
    try:
        cities = db_service.client.collection('cities').get_full_list()
        result = []
        for city in cities:
            places = db_service.client.collection('kebab_places').get_list(
                1, 50,
                query_params={
                    'filter': f'city="{city.id}"',
                    'fields': 'lat,lng',
                }
            )
            lats, lngs = [], []
            for p in places.items:
                la = getattr(p, 'lat', None)
                lo = getattr(p, 'lng', None)
                if la and lo:
                    try:
                        lats.append(float(la))
                        lngs.append(float(lo))
                    except (ValueError, TypeError):
                        pass
            if lats and lngs:
                result.append({
                    'name': city.name,
                    'slug': getattr(city, 'slug', city.name.lower()),
                    'lat': round(sum(lats) / len(lats), 5),
                    'lng': round(sum(lngs) / len(lngs), 5),
                    'count': len(lats),
                })
        resp = jsonify({'status': 'success', 'data': result})
        resp.headers['Cache-Control'] = 'public, max-age=86400'
        return resp
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/last-update')
def get_last_update():
    """Get the last update time for any city"""
    try:
        print("\n=== DEBUG: Getting last update ===")
        last_update = db_service.get_most_recent_update()
        update_interval = int(os.getenv('DATABASE_UPDATE_INTERVAL_DAYS', 7))
        current_time = datetime.now().astimezone()  # Make timezone-aware
        
        # Auto-updates disabled
        if last_update and (current_time - last_update.astimezone()) > timedelta(days=update_interval):
            print(f"Data is potentially stale (last update: {last_update}, current: {current_time}) but auto-update is disabled.")
            
            # Return actual last update rather than pretending it updated right now
            return jsonify({
                'status': 'success',
                'last_update': last_update.isoformat(),
                'update_interval_days': update_interval,
                'message': 'Data refresh is manual-only'
            })
            
        if last_update:
            print(f"Got last_update from DB service: {last_update}")
            
            # Calculate exactly how much time is left in the 7-day window
            time_passed = current_time - last_update.astimezone()
            interval_timedelta = timedelta(days=update_interval)
            
            # If we're somehow still in this block but past the interval, safety catch
            if time_passed > interval_timedelta:
                time_passed = interval_timedelta

            # We send the exact last update time so the frontend accurately computes the difference
            return jsonify({
                'status': 'success',
                'last_update': last_update.isoformat(),
                'update_interval_days': update_interval
            })
        else:
            print("No last_update found - but auto-update is disabled.")
            
            return jsonify({
                'status': 'success',
                'last_update': current_time.isoformat(),
                'update_interval_days': update_interval,
                'message': 'Manual data load required'
            })
    except Exception as e:
        print(f"Error in /api/last-update: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# --- START: NEW AI ENDPOINTS ---

@app.route('/api/rankings/<city>/ai')
@cache.cached(timeout=300, query_string=True)
def get_city_rankings_with_ai(city):
    """Get kebab rankings with AI insights using bulk fetching"""
    try:
        # Get language and limit from query parameters
        lang = request.args.get('lang', 'pl')
        limit = min(int(request.args.get('limit', 10)), 500)
        
        # Get basic rankings
        rankings = db_service.get_city_rankings(city, limit)
        if not rankings:
            return jsonify({'status': 'success', 'data': []})
            
        # Enrich with AI data for TOP 20 ONLY to ensure performance and stay under request limits
        google_ids = [k['google_place_id'] for k in rankings[:20]]
        ai_data_map = db_service.get_ai_for_places(google_ids)
        
        for kebab in rankings:
            ai_data = ai_data_map.get(kebab['google_place_id'])
            
            if ai_data:
                kebab['has_ai_analysis'] = True
                kebab['ai_score'] = ai_data.get('ai_score')
                kebab['ai_summary'] = translate_ai_summary(ai_data.get('ai_summary', ''), lang)
                kebab['ai_confidence'] = ai_data.get('confidence_score')
                
                analysis_data = ai_data.get('analysis_data', {})
                kebab['ai_insights'] = {
                    'sentiment': analysis_data.get('sentiment_analysis', {}).get('score', 0),
                    'trend': analysis_data.get('trend_analysis', {}).get('trend', 'stable'),
                    'authenticity': analysis_data.get('authenticity_analysis', {}).get('authenticity_score', 100)
                }
            else:
                kebab['has_ai_analysis'] = False
                kebab['ai_score'] = kebab.get('rank_score')
            
            # Ensure ai_rank exists for backward compatibility
            kebab['ai_rank'] = kebab.get('city_rank', 0)
        
        return jsonify({'status': 'success', 'data': rankings})
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/ai/insights/<place_id>')
def get_ai_insights(place_id):
    """Get AI insights for a specific kebab place"""
    try:
        kebab_place_id = db_service.get_place_id(place_id)
        
        if not kebab_place_id:
            return jsonify({'status': 'error', 'message': 'Place not found'}), 404
        
        ai_updater = AIDataUpdater(db_service, google_service, os.getenv('OPENAI_API_KEY'))
        insights = ai_updater.get_ai_insights_for_display(kebab_place_id)
        
        if not insights:
            return jsonify({
                'status': 'success',
                'data': None,
                'message': 'No AI analysis available yet'
            })
        
        return jsonify({'status': 'success', 'data': insights})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/ai/summary/<city>')
def get_city_ai_summary(city):
    """Get AI summary for entire city"""
    try:
        city_summary = db_service.get_city_ai_summary(city)
        if not city_summary:
            return jsonify({'status': 'success', 'data': {'message': 'No AI analysis available for this city yet'}})
        
        return jsonify({'status': 'success', 'data': city_summary})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/ai/update/<city>', methods=['POST'])
def trigger_ai_update(city):
    """Trigger AI update for a city (admin endpoint)"""
    try:
        auth_key = request.headers.get('Authorization')
        if auth_key != f"Bearer {os.getenv('ADMIN_KEY')}":
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
        if not os.getenv('OPENAI_API_KEY'):
            return jsonify({'status': 'error', 'message': 'OpenAI API key not configured'}), 500
        
        # Use the enhanced service for fetching reviews for AI
        g_service_enhanced = GooglePlacesEnhancedService(os.getenv('GOOGLE_API_KEY'))
        ai_updater = AIDataUpdater(db_service, g_service_enhanced, os.getenv('OPENAI_API_KEY'))
        
        thread = threading.Thread(
            target=ai_updater.update_ai_analysis_for_city,
            args=(city, 10) # Limit to 10 per run as an example
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({'status': 'success', 'message': f'AI analysis started for {city}'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# --- END: NEW AI ENDPOINTS ---


@app.route('/blog')
def blog_index():
    """Blog listing page"""
    articles = [
        {"slug": "najlepszy-kebab-krakow", "title": "Najlepszy kebab w Krakowie – TOP 10", "excerpt": "Ranking 10 najlepszych kebabów w Krakowie wraz z poradami i cenami.", "cover": "/static/img/blog/krakow.jpg", "date": "2025-06-16"},
        {"slug": "ranking-kebabow-warszawa", "title": "Ranking kebabów w Warszawie 2025", "excerpt": "Sprawdź, które lokale w stolicy są naprawdę warte kolejki.", "cover": "/static/img/blog/warszawa.jpg", "date": "2025-06-14"},
        {"slug": "najlepszy-kebab-lublin", "title": "Najlepszy kebab w Lublinie – Kraft i Nocne Życie", "excerpt": "Od studenckich klasyków po rzemieślnicze sztosy. Sprawdź, gdzie zjeść w Lublinie!", "cover": "/static/img/blog/lublin.png", "date": "2025-06-25"},
        {"slug": "najlepszy-kebab-bydgoszcz", "title": "Najlepszy kebab w Bydgoszczy – Kraft i Nocne Gastro", "excerpt": "Gdzie zjeść w Bydgoszczy? Przewodnik po najlepszych kebabach: od Maestro po legendy Fordonu.", "cover": "/static/img/blog/bydgoszcz.png", "date": "2025-06-24"},
        {"slug": "najlepszy-kebab-lodz", "title": "Najlepszy kebab w Łodzi – Kraftowa Rewolucja", "excerpt": "Łódź kebabem stoi! Sprawdź, gdzie zjesz najlepsze rzemieślnicze mięso i wegańskie nowości.", "cover": "/static/img/blog/lodz.png", "date": "2025-06-22"},
        {"slug": "najlepszy-kebab-szczecin", "title": "Najlepszy kebab w Szczecinie – Od Bar Rab po Kraft", "excerpt": "Odkryj ewolucję szczecińskiego street foodu – od nostalgicznych legend po nowoczesne, rzemieślnicze rarytasy.", "cover": "/static/img/blog/szczecin.png", "date": "2025-06-20"},
        {"slug": "najlepszy-kebab-katowice", "title": "Najlepszy kebab w Katowicach – Kraft, Berlin i Friz", "excerpt": "Gastronomiczna transformacja Śląska – odkryj najlepsze rzemieślnicze kebaby w Katowicach.", "cover": "/static/img/blog/katowice.png", "date": "2025-06-18"},
        {"slug": "najlepszy-kebab-wroclaw", "title": "Najlepszy kebab we Wrocławiu – TOP 10", "excerpt": "Odkryj najlepsze lokale we Wrocławiu, w tym miejsce nr 1 w skali całego kraju!", "cover": "/static/img/blog/wroclaw.jpeg", "date": "2025-06-15"},
        {"slug": "gdzie-na-kebaba", "title": "Gdzie na kebaba? Ogólnopolski przewodnik", "excerpt": "Praktyczne wskazówki i linki do rankingów ponad 50 miast.", "cover": "/static/img/blog/przewodnik.jpg", "date": "2025-06-12"},
        {"slug": "ai-sentiment-analysis", "title": "AI Sentiment Analysis dla Recenzji Restauracyjnych", "excerpt": "Czy wiesz, że sztuczna inteligencja rewolucjonizuje sposób, w jaki oceniane są kebaby? Sprawdź najnowsze trendy.", "cover": "/static/img/blog/guide.jpg", "date": "2026-04-08"},
        {"slug": "rynek-kebabow-w-polsce-statystyki-2026", "title": "Rynek Kebabów w Polsce – Statystyki 2026", "excerpt": "Kebab = 21% zamówień online, ~2,5 mld PLN wartości rynku, 25 000 lokali. 55+ punktów danych z Pyszne.pl, GUS i PMR.", "cover": "/static/img/blog/kebab-statystyki-rynek-2026.webp", "date": "2026-04-28"},
    ]
    return render_template('blog/index.html', articles=articles,
                         page_title="Blog Kebab Rank - Porady, Rankingi i Ciekawostki o Kebabach",
                         page_description="Najnowsze rankingi kebabów, porady foodies i kulinarne odkrycia z całej Polski. Sprawdź gdzie zjeść najlepszy rzemieślniczy kebab w Twoim mieście.")


@app.route('/blog/<slug>')
def blog_page(slug):
    """Individual blog post pages"""
    try:
        current_date = datetime.now().strftime('%d.%m.%Y')
        
        # SEO descriptors for standard slugs
        seo_data = {
            'najlepszy-kebab-krakow': {
                'title': "Najlepszy Kebab w Krakowie 2026 - Ranking TOP 10 | Kebab Rank",
                'desc': "Szukasz najlepszego kebaba w Krakowie? Sprawdź nasz aktualny ranking rzemieślniczych lokali. Kraftowe mięso, autentyczne sosy i opinie AI."
            },
            'ranking-kebabow-warszawa': {
                'title': "Ranking Kebabów w Warszawie 2026 - TOP 10 Miejsc | Kebab Rank",
                'desc': "Gdzie na najlepszy kebab w Warszawie? Przeczytaj nasz test 10 topowych lokali w stolicy. Od legendarnych budek po nowoczesny kraft."
            },
            'najlepszy-kebab-lublin': {
                'title': "Najlepszy Kebab w Lublinie - Ranking i Opinie 2026",
                'desc': "Odkryj smaki Lublina! Ranking najlepszych kebabów rzemieślniczych i studenckich klasyków wspierany analizą AI."
            },
            'najlepszy-kebab-bydgoszcz': {
                'title': "Najlepszy Kebab w Bydgoszczy - Gdzie Zjeść? Ranking 2026",
                'desc': "Przewodnik po najlepszych kebabach w Bydgoszczy. Sprawdź, które lokale cieszą się najwyższym uznaniem mieszkańców i turystów."
            },
            'najlepszy-kebab-lodz': {
                'title': "Najlepszy Kebab w Łodzi - Ranking Rzemieślniczych Lokali 2026",
                'desc': "Łódź kebabem stoi! Sprawdź ranking najlepszego mięsa i najoryginalniejszych sosów w łódzkich kebabowniach."
            },
            'najlepszy-kebab-szczecin': {
                'title': "Najlepszy Kebab w Szczecinie - Ranking Legend i Nowości 2026",
                'desc': "Od Bar Rab po nowoczesny kraft - zobacz jakie kebaby w Szczecinie są obecnie numerem jeden według opinii Google."
            },
            'najlepszy-kebab-katowice': {
                'title': "Najlepszy Kebab w Katowicach - Ranking Silesia 2026",
                'desc': "Katowicka scena kebabowa w pigułce. Sprawdź gdzie zjeść najlepszy rzemieślniczy kebab w sercu aglomeracji."
            },
            'najlepszy-kebab-wroclaw': {
                'title': "Najlepszy Kebab we Wrocławiu - Ranking TOP 10 2026 | Kebab Rank",
                'desc': "Wrocław to dom dla najlepszego kebaba w Polsce! Sprawdź nasz ranking TOP 10 i znajdź swój ulubiony smak."
            },
            'gdzie-na-kebaba': {
                'title': "Gdzie na Kebaba? Ogólnopolski Przewodnik i Ranking 2026",
                'desc': "Praktyczne wskazówki jak rozpoznać dobry kebab i linki do rankingów w ponad 50 miastach Polski."
            },
            'ai-sentiment-analysis': {
                'title': "AI Sentiment Analysis dla Kebabów - Przewodnik 2026 | Kebab Rank",
                'desc': "Kompletny przewodnik po AI sentiment analysis. Dowiedz się, jak sztuczna inteligencja zmienia ocenianie i jak wpływa na ranking restauracji w Polsce."
            },
            'rynek-kebabow-w-polsce-statystyki-2026': {
                'title': "Rynek Kebabów w Polsce – Statystyki 2026: 55+ Punktów Danych | Kebab Rank",
                'desc': "Kompletny raport: kebab = 21% zamówień online, wartość rynku ~2,5 mld PLN, 25 000 lokali. Dane z Pyszne.pl, GUS i PMR Market Experts."
            }
        }

        current_seo = seo_data.get(slug, {
            'title': f"{slug.replace('-', ' ').title()} | Blog Kebab Rank",
            'desc': f"Przeczytaj artykuł o {slug.replace('-', ' ')} na blogu Kebab Rank."
        })

        if slug == 'najlepszy-kebab-krakow':
            city = "Kraków"
            rankings = db_service.get_city_rankings(city)
            top_kebabs = rankings[:10] if rankings else []
            return render_template(f'blog/{slug}.html', top_kebabs=top_kebabs, current_date=current_date,
                                 page_title=current_seo['title'], page_description=current_seo['desc'])

        if slug == 'ranking-kebabow-warszawa':
            city = "Warszawa"
            rankings = db_service.get_city_rankings(city, limit=10)
            return render_template(f'blog/{slug}.html', kebab_places=rankings, current_date=current_date,
                                 page_title=current_seo['title'], page_description=current_seo['desc'])
        
        if slug in ['najlepszy-kebab-lublin', 'najlepszy-kebab-bydgoszcz', 'najlepszy-kebab-lodz', 
                    'najlepszy-kebab-szczecin', 'najlepszy-kebab-katowice', 'najlepszy-kebab-wroclaw']:
            city_map = {
                'najlepszy-kebab-lublin': 'Lublin',
                'najlepszy-kebab-bydgoszcz': 'Bydgoszcz',
                'najlepszy-kebab-lodz': 'Łódź',
                'najlepszy-kebab-szczecin': 'Szczecin',
                'najlepszy-kebab-katowice': 'Katowice',
                'najlepszy-kebab-wroclaw': 'Wrocław'
            }
            city = city_map[slug]
            rankings = db_service.get_city_rankings(city)
            top_kebabs = rankings[:10] if rankings else []
            return render_template(f'blog/{slug}.html', top_kebabs=top_kebabs, current_date=current_date,
                                 page_title=current_seo['title'], page_description=current_seo['desc'])
        
        return render_template(f'blog/{slug}.html', current_date=current_date,
                             page_title=current_seo['title'], page_description=current_seo['desc'])
    except Exception as e:
        print(f"Error rendering blog page {slug}: {e}")
        return render_template('blog/404.html'), 404


@app.route('/sitemap.xml')
@cache.cached(timeout=21600)  # 6h — sitemapa zmienia się tylko przy update'cie danych
def sitemap():
    """
    Sitemapa generowana z bazy i z katalogu bloga.

    Wcześniej był to statyczny plik, który zwietrzał: lastmod pokazywał
    2025-06 przy danych aktualizowanych co tydzień, a nowe miasta i artykuły
    trzeba było dopisywać ręcznie (jeden artykuł wypadł). Google widząc
    stary lastmod rzadziej wraca po nowe treści.
    """
    import xml.sax.saxutils as su

    BASE = 'https://www.kebabrank.com'
    PL_MAP = {'ł': 'l', 'ó': 'o', 'ą': 'a', 'ę': 'e', 'ć': 'c',
              'ń': 'n', 'ś': 's', 'ź': 'z', 'ż': 'z'}

    def slugify(name):
        s = name.lower()
        for char, repl in PL_MAP.items():
            s = s.replace(char, repl)
        return s.replace(' ', '-')

    today = datetime.now().strftime('%Y-%m-%d')

    # Data ostatniej aktualizacji rankingów — wspólny lastmod dla stron miast
    try:
        last_update = db_service.get_most_recent_update()
        data_date = last_update.strftime('%Y-%m-%d') if last_update else today
    except Exception as e:
        print(f"[SITEMAP] Nie udało się pobrać daty update'u: {e}")
        data_date = today

    urls = [
        (f'{BASE}/', today, 'daily', '1.0'),
        (f'{BASE}/blog', today, 'weekly', '0.8'),
        (f'{BASE}/privacy', '2026-01-01', 'yearly', '0.3'),
        (f'{BASE}/terms', '2026-01-01', 'yearly', '0.3'),
    ]

    # Strony miast — prosto z bazy, więc nowe miasto trafia tu automatycznie
    try:
        for city in db_service.get_cities():
            urls.append((f"{BASE}/kebab-{slugify(city['name'])}",
                         data_date, 'weekly', '0.9'))
    except Exception as e:
        print(f"[SITEMAP] Nie udało się pobrać miast: {e}")

    # Artykuły bloga — z katalogu szablonów, więc nowy plik trafia tu automatycznie
    try:
        blog_dir = os.path.join(app.root_path, 'templates', 'blog')
        for fname in sorted(os.listdir(blog_dir)):
            if not fname.endswith('.html') or fname in ('index.html', '404.html'):
                continue
            mtime = os.path.getmtime(os.path.join(blog_dir, fname))
            urls.append((f'{BASE}/blog/{fname[:-5]}',
                         datetime.fromtimestamp(mtime).strftime('%Y-%m-%d'),
                         'monthly', '0.7'))
    except Exception as e:
        print(f"[SITEMAP] Nie udało się odczytać bloga: {e}")

    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, freq, prio in urls:
        parts.append(
            f'  <url><loc>{su.escape(loc)}</loc><lastmod>{lastmod}</lastmod>'
            f'<changefreq>{freq}</changefreq><priority>{prio}</priority></url>'
        )
    parts.append('</urlset>')

    return Response('\n'.join(parts), mimetype='application/xml')


@app.route('/favicon.ico') 
def favicon():
    """Serve favicon with correct headers"""
    response = send_from_directory('static/img', 'favicon.ico')
    response.headers['Content-Type'] = 'image/x-icon'
    response.headers['Cache-Control'] = 'public, max-age=86400'
    return response

@app.route('/apple-touch-icon.png')
def apple_touch_icon():
    return send_from_directory('static/img', 'apple-touch-icon.png')

@app.route('/favicon-32x32.png')
def favicon32():
    return send_from_directory('static/img', 'favicon-32x32.png')

@app.route('/favicon-16x16.png') 
def favicon16():
    return send_from_directory('static/img', 'favicon-16x16.png')

@app.route('/site.webmanifest')
def webmanifest():
    return send_from_directory('static/img', 'site.webmanifest')

@app.route('/robots.txt')
def robots():
    """Serve robots.txt"""
    return send_from_directory('static', 'robots.txt')


@app.route('/api/update/force', methods=['POST'])
def force_update():
    """Force update all data (admin endpoint)"""
    try:
        auth_key = request.headers.get('Authorization')
        if auth_key != f"Bearer {os.getenv('ADMIN_KEY')}":
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
        data_updater.update_all_cities()
        return jsonify({'status': 'success', 'message': 'Update initiated'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
# Add this debug version to your app.py temporarily

@app.route('/api/rankings/<city>/ai/debug')
def debug_city_rankings_with_ai(city):
    """Debug version of AI rankings endpoint"""
    try:
        rankings = db_service.get_city_rankings(city)
        print(f"\n=== DEBUG: Found {len(rankings)} kebabs for {city} ===")
        
        for kebab in rankings:
            print(f"\nKebab: {kebab['name']}")
            print(f"  Google Place ID: {kebab.get('google_place_id', 'MISSING')}")
            
            # First, get the kebab_place_id from kebab_places table
            place_response = db_service.client.table('kebab_places').select('id').eq(
                'google_place_id', kebab['google_place_id']
            ).execute()
            
            if place_response.data:
                kebab_place_id = place_response.data[0]['id']
                print(f"  Kebab Place ID: {kebab_place_id}")
                
                # Now query ai_analysis with the correct ID
                ai_response = db_service.client.table('ai_analysis').select(
                    'ai_score, ai_summary, confidence_score, analysis_data'
                ).eq('kebab_place_id', kebab_place_id).order(
                    'created_at', desc=True
                ).limit(1).execute()
                
                if ai_response.data:
                    print(f"  ✅ AI data found!")
                    ai_data = ai_response.data[0]
                    kebab['has_ai_analysis'] = True
                    kebab['ai_score'] = ai_data.get('ai_score')
                    kebab['ai_summary'] = ai_data.get('ai_summary')
                    print(f"  AI Score: {kebab['ai_score']}")
                    print(f"  AI Summary: {kebab['ai_summary'][:50]}...")
                else:
                    print(f"  ❌ No AI data found")
                    kebab['has_ai_analysis'] = False
            else:
                print(f"  ❌ Kebab place not found in database")
                kebab['has_ai_analysis'] = False

        return jsonify({'status': 'success', 'data': rankings})
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('blog/404.html'), 404

@app.route('/api/history/rankings/<city>')
def get_historical_rankings(city):
    """Get historical rankings for a city"""
    try:
        history = db_service.get_city_rankings_history(city)
        
        return jsonify({
            'status': 'success',
            'city': city,
            'data': history
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/debug/rankings/<city>')
def debug_rankings(city):
    """Debug endpoint to check rank change data"""
    try:
        # Get rankings with debug info
        rankings = db_service.get_city_rankings(city, limit=5)
        
        # Format for easy reading
        debug_info = {
            'city': city,
            'total_kebabs': len(rankings),
            'rankings': []
        }
        
        for kebab in rankings:
            debug_info['rankings'].append({
                'name': kebab['name'],
                'city_rank': kebab.get('city_rank'),
                'rank_change': kebab.get('rank_change'),
                'is_new': kebab.get('is_new'),
                'rank_change_indicator': kebab.get('rank_change_indicator'),
                'has_rank_change_data': 'rank_change' in kebab
            })
        
        return jsonify({
            'status': 'success',
            'debug': debug_info
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint for Docker and monitoring"""
    try:
        # Basic health check - just return 200 if app is running
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'kebab-rank-api'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500



@app.route('/eu194yp2dtsh23cy4aapz6pequxv3f2w.txt')
def index_now_verification():
    """Verify IndexNow for search engines"""
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'eu194yp2dtsh23cy4aapz6pequxv3f2w.txt')


def _build_email_html(kebab_name=None, kebab_rating=None, kebab_address=None, kebab_gmaps_url=None, city=None):
    if kebab_name:
        rating_stars = ('★' * round(float(kebab_rating))) if kebab_rating else ''
        kebab_block = f"""
        <div style="background:#fffbeb;border:2px solid #fbbf24;border-radius:12px;padding:20px 24px;margin:24px 0;">
          <p style="margin:0 0 4px;font-size:12px;color:#92400e;font-weight:600;letter-spacing:.05em;">TWÓJ LOSOWY KEBAB</p>
          <p style="margin:0 0 8px;font-size:22px;font-weight:800;color:#1e293b;">{kebab_name}</p>
          {"<p style='margin:0 0 4px;font-size:18px;color:#d97706;font-weight:700;'>"+rating_stars+" "+str(kebab_rating)+"</p>" if kebab_rating else ''}
          {"<p style='margin:0 0 16px;font-size:13px;color:#64748b;'>"+kebab_address+"</p>" if kebab_address else ''}
          {"<a href='"+kebab_gmaps_url+"' style='display:inline-block;padding:11px 24px;background:linear-gradient(135deg,#1d4ed8,#7c3aed);color:#fff;font-size:14px;font-weight:700;text-decoration:none;border-radius:10px;'>🗺️ Prowadź do kebaba</a>" if kebab_gmaps_url else ''}
        </div>
        <p style="color:#475569;font-size:14px;">Subskrybujesz też powiadomienia o zmianach w rankingu — poinformujemy Cię gdy pojawi się nowy lider lub duże zmiany.</p>"""
        subject_preview = f"Twój losowy kebab: {kebab_name}"
    else:
        city_txt = f" w <strong>{city}</strong>" if city else ""
        kebab_block = f"""
        <p style="color:#1e293b;font-size:15px;line-height:1.7;">Zapisałeś się na powiadomienia KebabRank{city_txt}. Wyślemy Ci maila gdy:</p>
        <ul style="color:#475569;font-size:14px;line-height:2;padding-left:20px;">
          <li>Pojawi się <strong>nowy nr 1</strong> w rankingu</li>
          <li>Nowe miejsce wejdzie do top 10</li>
          <li>Nastąpi duży wzrost lub spad popularnej kebabowni</li>
        </ul>"""
        subject_preview = "Jesteś na liście KebabRank"

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head><body style="margin:0;padding:0;background:#f8fafc;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8fafc;padding:32px 16px;">
      <tr><td align="center">
        <table width="560" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08);">
          <tr><td style="background:linear-gradient(135deg,#1e293b,#0f172a);padding:28px 32px;text-align:center;">
            <p style="margin:0;font-size:26px;font-weight:900;color:#fbbf24;letter-spacing:-.5px;">🥙 KebabRank</p>
            <p style="margin:6px 0 0;font-size:13px;color:#94a3b8;">kebabrank.com</p>
          </td></tr>
          <tr><td style="padding:32px;">
            <p style="margin:0 0 16px;font-size:20px;font-weight:800;color:#1e293b;">{subject_preview} 🎉</p>
            {kebab_block}
            <hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0;">
            <p style="color:#94a3b8;font-size:12px;margin:0;">Otrzymujesz tego maila bo podałeś adres na <a href="https://kebabrank.com" style="color:#fbbf24;">kebabrank.com</a>.<br>
            Aby się wypisać, odpowiedz na tego maila z treścią "wypisz".</p>
          </td></tr>
        </table>
      </td></tr>
    </table></body></html>"""


def _send_email_async(to_email, subject, html):
    smtp_host = os.environ.get('SMTP_HOST', '')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_pass = os.environ.get('SMTP_PASS', '')
    from_name = os.environ.get('FROM_NAME', 'KebabRank')
    from_email = os.environ.get('FROM_EMAIL', smtp_user)
    if not smtp_host or not smtp_user or not smtp_pass:
        print(f'[EMAIL] Brak konfiguracji SMTP (SMTP_HOST={smtp_host!r}, SMTP_USER={smtp_user!r})')
        return
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f'{from_name} <{from_email}>'
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        with smtplib.SMTP(smtp_host, smtp_port) as srv:
            srv.ehlo()
            srv.starttls()
            srv.login(smtp_user, smtp_pass)
            srv.sendmail(from_email, to_email, msg.as_string())
        print(f'[EMAIL] OK → {to_email}')
    except Exception as e:
        print(f'[EMAIL] BŁĄD → {e}')


def _notify_telegram(msg):
    token   = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
    if not token or not chat_id:
        return
    try:
        requests.post(
            f'https://api.telegram.org/bot{token}/sendMessage',
            json={'chat_id': chat_id, 'text': msg, 'parse_mode': 'HTML'},
            timeout=8
        )
    except Exception as e:
        print(f'[TELEGRAM] BŁĄD → {e}')


@app.route('/api/test-email')
def test_email():
    if os.environ.get('FLASK_ENV') == 'production':
        return jsonify({'error': 'disabled in production'}), 403
    to = request.args.get('to', '')
    if not to:
        return jsonify({'error': 'Podaj ?to=twoj@email.com'}), 400
    html = _build_email_html(kebab_name='Testowy Kebab Ali', kebab_rating='4.8',
                             kebab_address='ul. Testowa 1, Kraków',
                             kebab_gmaps_url='https://kebabrank.com')
    _send_email_async(to, 'Test KebabRank 🥙', html)
    return jsonify({'sent': True, 'to': to, 'check': 'sprawdź logi konsoli po błąd'})


@app.route('/api/subscribe', methods=['POST'])
def subscribe_email():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    source = (data.get('source') or 'unknown')[:50]
    kebab_name    = data.get('kebab_name') or None
    kebab_rating  = data.get('kebab_rating') or None
    kebab_address = data.get('kebab_address') or None
    kebab_gmaps   = data.get('kebab_gmaps_url') or None
    if not email or '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'error': 'invalid_email'}), 400
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'subscribers.db')
    import sqlite3
    conn = sqlite3.connect(db_path)
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS subscribers
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         email TEXT UNIQUE NOT NULL,
                         source TEXT,
                         created_at TEXT)''')
        result = conn.execute('INSERT OR IGNORE INTO subscribers (email, source, created_at) VALUES (?,?,?)',
                     (email, source, datetime.now().isoformat()))
        conn.commit()
        is_new = result.rowcount > 0
        print(f'[SUBSCRIBE] email={email} source={source} is_new={is_new}')

        if is_new:
            city = None
            if source.startswith('city_watch:'):
                city = source.split(':', 1)[1] or None
            if kebab_name:
                subject = f'Twój losowy kebab: {kebab_name} 🥙'
            elif city:
                subject = f'Obserwujesz {city} na KebabRank 🥙'
            else:
                subject = 'Jesteś na liście KebabRank 🥙'
            html = _build_email_html(kebab_name, kebab_rating, kebab_address, kebab_gmaps, city)
            threading.Thread(target=_send_email_async, args=(email, subject, html), daemon=True).start()

            if kebab_name:
                tg_source = f'🎲 Ruletka\n🥙 {kebab_name}' + (f' ⭐{kebab_rating}' if kebab_rating else '') + (f'\n📍 {kebab_address}' if kebab_address else '')
            elif city:
                tg_source = f'👁 Obserwuj miasto: <b>{city}</b>'
            else:
                tg_source = '📬 Newsletter (footer)'
            tg_msg = f'🎯 <b>Nowa subskrypcja</b>\n📧 {email}\n{tg_source}\n🕐 {datetime.now().strftime("%H:%M")}'
            threading.Thread(target=_notify_telegram, args=(tg_msg,), daemon=True).start()

        return jsonify({'ok': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/request-city', methods=['POST'])
def request_city():
    data = request.get_json(silent=True) or {}
    city       = (data.get('city') or '').strip()[:100]
    voivodeship= (data.get('voivodeship') or '').strip()[:60]
    email      = (data.get('email') or '').strip().lower()
    if not city or not email or '@' not in email:
        return jsonify({'error': 'invalid_data'}), 400

    # Check if city already exists in the ranking
    try:
        _polish = str.maketrans('łóąęćńśźż', 'loacensza' if False else 'loacenszz')
        def _norm(s):
            t = s.lower().strip()
            return t.translate(str.maketrans('łóąęćńśźż', 'loaecnszz'))
        existing = db_service.get_cities()
        city_names = [c.get('name', '') for c in (existing.get('data') or [])]
        if any(_norm(cn) == _norm(city) for cn in city_names):
            return jsonify({'error': 'city_exists', 'message': 'To miasto jest już w naszym rankingu!'}), 409
    except Exception:
        pass  # if check fails, allow submission through
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'subscribers.db')
    import sqlite3
    conn = sqlite3.connect(db_path)
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS city_requests
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         city TEXT, voivodeship TEXT,
                         email TEXT, created_at TEXT)''')
        conn.execute('INSERT INTO city_requests (city, voivodeship, email, created_at) VALUES (?,?,?,?)',
                     (city, voivodeship, email, datetime.now().isoformat()))
        conn.commit()
    finally:
        conn.close()

    # Email do użytkownika
    user_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head>
    <body style="margin:0;padding:0;background:#f8fafc;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8fafc;padding:32px 16px;">
      <tr><td align="center">
        <table width="560" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08);">
          <tr><td style="background:linear-gradient(135deg,#1e293b,#0f172a);padding:28px 32px;text-align:center;">
            <p style="margin:0;font-size:26px;font-weight:900;color:#fbbf24;">🥙 KebabRank</p>
            <p style="margin:6px 0 0;font-size:13px;color:#94a3b8;">kebabrank.com</p>
          </td></tr>
          <tr><td style="padding:32px;">
            <p style="margin:0 0 16px;font-size:20px;font-weight:800;color:#1e293b;">Zgłoszenie przyjęte! 🎉</p>
            <p style="color:#475569;font-size:15px;line-height:1.7;">Dziękujemy za zgłoszenie <strong>{city}</strong>
            {f'({voivodeship})' if voivodeship else ''} do KebabRank!</p>
            <div style="background:#fffbeb;border:2px solid #fbbf24;border-radius:12px;padding:18px 20px;margin:20px 0;">
              <p style="margin:0;font-size:14px;color:#92400e;line-height:1.6;">
                Rozpatrzymy wniosek i zbierzemy dane o kebabowniach w Twoim mieście.<br>
                <strong>Poinformujemy Cię mailem gdy miasto zostanie dodane do rankingu.</strong>
              </p>
            </div>
            <p style="color:#94a3b8;font-size:13px;margin:0;">Zespół KebabRank •
              <a href="https://kebabrank.com" style="color:#fbbf24;">kebabrank.com</a></p>
          </td></tr>
        </table>
      </td></tr>
    </table></body></html>"""
    threading.Thread(target=_send_email_async,
                     args=(email, f'Zgłoszenie miasta {city} przyjęte 🥙', user_html),
                     daemon=True).start()

    # Powiadomienie dla admina — email
    admin_email = os.environ.get('FROM_EMAIL', '')
    if admin_email:
        admin_html = f"<p>Nowe zgłoszenie miasta:</p><ul><li><b>Miasto:</b> {city}</li><li><b>Województwo:</b> {voivodeship}</li><li><b>Email:</b> {email}</li></ul>"
        threading.Thread(target=_send_email_async,
                         args=(admin_email, f'[KebabRank] Nowe zgłoszenie: {city}', admin_html),
                         daemon=True).start()

    # Powiadomienie dla admina — Telegram
    tg_msg = (f'🏙 <b>Nowe zgłoszenie miasta</b>\n'
              f'📍 {city}' + (f', {voivodeship}' if voivodeship else '') +
              f'\n📧 {email}\n🕐 {datetime.now().strftime("%H:%M")}')
    threading.Thread(target=_notify_telegram, args=(tg_msg,), daemon=True).start()

    return jsonify({'ok': True}), 200


@app.route('/api/city-requests/export')
def export_city_requests():
    secret = request.args.get('key', '')
    if secret != os.environ.get('ADMIN_KEY', 'kebab2026'):
        return jsonify({'error': 'unauthorized'}), 401
    import sqlite3
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'subscribers.db')
    conn = sqlite3.connect(db_path)
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS city_requests
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         city TEXT, voivodeship TEXT,
                         email TEXT, created_at TEXT)''')
        rows = conn.execute('SELECT city, voivodeship, email, created_at FROM city_requests ORDER BY id DESC').fetchall()
        return jsonify({'count': len(rows),
                        'requests': [{'city': r[0], 'voivodeship': r[1], 'email': r[2], 'created_at': r[3]} for r in rows]})
    finally:
        conn.close()


@app.route('/api/subscribers/export')
def export_subscribers():
    secret = request.args.get('key', '')
    if secret != os.environ.get('ADMIN_KEY', 'kebab2026'):
        return jsonify({'error': 'unauthorized'}), 401
    import sqlite3
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'subscribers.db')
    if not os.path.exists(db_path):
        return jsonify({'count': 0, 'subscribers': []})
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute('SELECT email, source, created_at FROM subscribers ORDER BY id DESC').fetchall()
        data = [{'email': r[0], 'source': r[1], 'created_at': r[2]} for r in rows]
        return jsonify({'count': len(data), 'subscribers': data})
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)), threaded=True)
