# 🥙 KebabRank Poland - AI-Powered Kebab Ranking Platform

[![Website](https://img.shields.io/badge/Website-kebabrank.com-orange)](https://kebabrank.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Database-Supabase-purple)](https://supabase.com)
[![AI Powered](https://img.shields.io/badge/AI-OpenAI-brightgreen)](https://openai.com)

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Features](#features)
5. [Project Structure](#project-structure)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [Database Schema](#database-schema)
9. [API Endpoints](#api-endpoints)
10. [AI Integration](#ai-integration)
11. [Admin Management](#admin-management)
12. [Deployment](#deployment)
13. [Monitoring & Maintenance](#monitoring--maintenance)
14. [Development Workflow](#development-workflow)
15. [Troubleshooting](#troubleshooting)

---

## 🌟 Overview

KebabRank is Poland's first AI-powered kebab ranking platform that combines Google Places data with advanced sentiment analysis to provide the most comprehensive kebab rankings across 50+ Polish cities. The platform updates weekly and uses machine learning to detect fake reviews, analyze customer sentiment, and predict quality trends.

### Key Metrics
- **Coverage**: 50+ Polish cities
- **Kebabs Tracked**: 500+ establishments
- **Reviews Analyzed**: 10,000+ customer reviews
- **Update Frequency**: Weekly automated updates
- **AI Accuracy**: 95% sentiment analysis confidence

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                              │
│  HTML/CSS/JavaScript + Responsive Design + Multi-language    │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    Flask Backend                              │
│          API Routes + Business Logic + Caching               │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┬─────────────────────┐
        │                           │                      │
┌───────▼────────┐          ┌──────▼──────┐      ┌───────▼────────┐
│ Google Places  │          │  Supabase   │      │   OpenAI API   │
│      API       │          │  Database   │      │  GPT-3.5-turbo │
└────────────────┘          └─────────────┘      └────────────────┘
```

---

## 💻 Technology Stack

### Backend
- **Framework**: Flask 2.3.3 (Python 3.8+)
- **WSGI Server**: Gunicorn (production)
- **Task Queue**: Threading (for background updates)
- **API Integration**: 
  - Google Places API (place data & reviews)
  - OpenAI API (sentiment analysis)

### Frontend
- **Core**: Vanilla JavaScript (ES6+)
- **Styling**: Custom CSS with Flexbox/Grid
- **Icons**: Emoji-based UI elements
- **Localization**: Polish/English support

### Database
- **Primary**: Supabase (PostgreSQL)
- **Tables**: 
  - `cities` - City management
  - `kebab_places` - Restaurant data
  - `ratings_history` - Historical ratings
  - `ai_analysis` - AI insights
  - `cached_reviews` - Review storage

### Infrastructure
- **Domain**: kebabrank.com (Hostinger)
- **Server**: Hostinger VPS KV2
- **Container**: Docker & Docker Compose
- **Reverse Proxy**: Nginx
- **SSL**: Let's Encrypt

### AI/ML Components
- **Sentiment Analysis**: TextBlob + Custom Polish NLP
- **Review Authentication**: Pattern matching algorithms
- **Trend Prediction**: Time-series analysis
- **Language Processing**: Multi-language support (PL/EN)

---

## ✨ Features

### Core Features
1. **City-based Rankings** - Search and view top 10 kebabs per city
2. **Global Top 10** - Best kebabs across all of Poland
3. **Smart Scoring Algorithm**:
   - 75% Google rating
   - 15% Review count (logarithmic)
   - 10% AI sentiment (when available)

### AI-Powered Features
1. **Sentiment Analysis** - Analyzes customer emotions in reviews
2. **Fake Review Detection** - Identifies suspicious review patterns
3. **Trend Analysis** - Tracks quality improvements/declines
4. **Customer Insights** - Demographics and visit patterns
5. **Aspect Analysis** - What customers love/hate (meat, sauce, service)

### SEO & Marketing
1. **City-specific URLs** - /krakow, /warszawa etc.
2. **Blog System** - SEO-optimized content
3. **Sitemap Generation** - Auto-updated
4. **Social Media Integration** - Instagram, TikTok, Facebook

### Admin Features
1. **City Management** - Add/remove cities
2. **Data Updates** - Manual/automatic refresh
3. **AI Processing** - Batch analysis tools
4. **Ranking Fixes** - Recalculation tools

---

## 📁 Project Structure

```
kebab-rank/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in git)
├── docker-compose.prod.yml   # Production Docker config
│
├── services/                 # Business logic layer
│   ├── __init__.py
│   ├── database.py          # Supabase interface
│   ├── google_places.py     # Google API wrapper
│   ├── google_places_enhanced.py  # Review fetching
│   ├── ranking.py           # Scoring algorithm
│   ├── data_updater.py      # Update orchestration
│   ├── ai_service.py        # AI analysis core
│   └── ai_data_updater.py   # AI data management
│
├── templates/               # HTML templates
│   ├── index.html          # Homepage
│   ├── base.html           # Base template
│   └── blog/               # Blog templates
│       ├── index.html
│       ├── najlepszy-kebab-krakow.html
│       ├── ranking-kebabow-warszawa.html
│       └── gdzie-na-kebaba.html
│
├── static/                  # Static assets
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   ├── js/
│   │   └── app.js          # Frontend logic
│   └── img/
│       ├── logo.png
│       └── favicon.ico
│
├── management/              # Admin scripts
│   ├── add_city.py         # Add new city
│   ├── update_all_cities.py
│   ├── fix_rankings.py     # Fix ranking issues
│   ├── update_ai_analysis.py
│   └── generate_sitemap.py
│
└── database/               # SQL schemas
    └── schema.sql         # Database structure
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (via Supabase)
- Google Cloud account (for Places API)
- OpenAI account (for AI features)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kebab-rank.git
   cd kebab-rank
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Initialize database**
   - Create Supabase project
   - Run `database/schema.sql` in Supabase SQL editor

6. **Run the application**
   ```bash
   python app.py
   ```

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
# API Keys
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# Admin
ADMIN_KEY=your_secure_admin_key

# Settings
FLASK_ENV=development
DATABASE_UPDATE_INTERVAL_DAYS=7
```

### API Quotas & Limits
- **Google Places**: $200 free monthly credit
  - Place Search: $32/1000 requests
  - Place Details: $17/1000 requests
- **OpenAI**: Pay-as-you-go
  - GPT-3.5-turbo: $0.002/1K tokens
- **Supabase**: Free tier
  - 500MB database
  - 2GB bandwidth

---

## 🗄️ Database Schema

### Core Tables

#### cities
```sql
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### kebab_places
```sql
CREATE TABLE kebab_places (
    id SERIAL PRIMARY KEY,
    google_place_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    city_id INTEGER REFERENCES cities(id),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### ratings_history
```sql
CREATE TABLE ratings_history (
    id SERIAL PRIMARY KEY,
    kebab_place_id INTEGER REFERENCES kebab_places(id),
    rating DECIMAL(2, 1),
    total_reviews INTEGER,
    positive_percentage DECIMAL(5, 2),
    rank_score DECIMAL(5, 2),
    city_rank INTEGER,
    global_rank INTEGER,
    ai_score FLOAT,
    ai_confidence FLOAT,
    sentiment_score FLOAT,
    authenticity_score FLOAT,
    trend_momentum FLOAT,
    data_fetched_at TIMESTAMP DEFAULT NOW()
);
```

#### ai_analysis
```sql
CREATE TABLE ai_analysis (
    id SERIAL PRIMARY KEY,
    kebab_place_id INTEGER REFERENCES kebab_places(id),
    analysis_type VARCHAR(50),
    analysis_data JSONB,
    ai_score FLOAT,
    ai_summary TEXT,
    confidence_score FLOAT,
    review_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔌 API Endpoints

### Public Endpoints
```
GET /                           # Homepage
GET /<city-slug>               # City page (SEO-friendly)
GET /blog                      # Blog listing
GET /blog/<slug>               # Blog article

GET /api/cities                # List all cities
GET /api/rankings/<city>       # Get city rankings
GET /api/rankings/global       # Get global top 10
GET /api/last-update          # Get last update time
```

### AI-Enhanced Endpoints
```
GET /api/rankings/<city>/ai    # Rankings with AI insights
GET /api/ai/insights/<place_id> # Detailed AI analysis
GET /api/ai/summary/<city>     # City-wide AI summary
```

### Admin Endpoints (Protected)
```
POST /api/update/force         # Force update all data
POST /api/ai/update/<city>     # Trigger AI analysis
```

---

## 🤖 AI Integration

### Sentiment Analysis Pipeline
1. **Review Collection**: Fetch from Google Places API (max 5 reviews)
2. **Language Detection**: Identify Polish/English text
3. **Sentiment Scoring**: 
   - TextBlob for English
   - Custom dictionary for Polish
   - Combined score (-1 to +1)

### Fake Review Detection
- **Pattern Analysis**:
  - Very short generic reviews
  - No specific details mentioned
  - Multiple reviews from same author
  - Review bombing (temporal clustering)
- **Authenticity Score**: 0-100% confidence

### Trend Analysis
- **Time-series comparison**: Old vs new reviews
- **Momentum calculation**: Rate of change
- **Predictions**: Improving/Declining/Stable

### AI Scoring Formula
```python
ai_score = base_score + 
          (sentiment * 5) +           # ±5 points
          (authenticity_penalty) +     # -10 to 0 points
          (trend_momentum / 20) +      # ±5 points
          ((satisfaction - 50) / 10)   # ±5 points
```

---

## 👨‍💼 Admin Management

### Daily Tasks
```bash
# Check system health
python management/debug_system.py

# Add new city
python management/add_city.py "City Name"

# Update specific city
python management/update_single_city.py "Kraków"
```

### Weekly Tasks
```bash
# Update all cities
python management/update_all_cities.py

# Run AI analysis for major cities
python management/batch_ai_update.py

# Generate new sitemap
python management/generate_sitemap.py
```

### Troubleshooting
```bash
# Fix ranking issues
python management/fix_rankings.py

# Check specific city rankings
python management/check_rankings.py "Kraków"

# Verify AI data
python management/check_ai_data.py "Kraków"
```

---

## 🚢 Deployment

### Server Setup (Hostinger VPS)
1. **SSH Access**
   ```bash
   ssh root@your-server-ip
   ```

2. **Clone repository**
   ```bash
   cd /opt
   git clone https://github.com/yourusername/kebab-rank.git
   ```

3. **Docker setup**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Nginx configuration**
   ```nginx
   server {
       listen 80;
       server_name kebabrank.com www.kebabrank.com;
       
       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **SSL with Certbot**
   ```bash
   certbot --nginx -d kebabrank.com -d www.kebabrank.com
   ```

### Deployment Commands
```bash
# Deploy updates
cd /opt/kebab-rank
git pull
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker logs kebab-rank-app -f

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

---

## 📊 Monitoring & Maintenance

### Health Checks
- **Uptime Robot**: Monitor site availability
- **Google Analytics**: Track user behavior
- **Supabase Dashboard**: Database metrics
- **API Usage**:
  - Google Cloud Console for Places API
  - OpenAI Dashboard for GPT usage

### Backup Strategy
- **Database**: Supabase automatic daily backups
- **Code**: GitHub repository
- **Reviews Cache**: Weekly export to JSON

### Performance Optimization
- **Caching**: 7-day data refresh cycle
- **Rate Limiting**: 
  - 2-second delay between Google API calls
  - 5-second delay between cities
- **Database Indexing**: On frequently queried columns

---

## 🔄 Development Workflow

### Feature Development
1. **Local Development**
   ```bash
   git checkout -b feature/new-feature
   # Make changes
   python app.py  # Test locally
   ```

2. **Testing**
   ```bash
   # Run specific city test
   python test_city.py "Kraków"
   
   # Check AI analysis
   python update_ai_analysis.py "Kraków" --limit 1
   ```

3. **Deployment**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/new-feature
   # Create PR and merge
   
   # On server
   cd /opt/kebab-rank
   git pull
   docker-compose -f docker-compose.prod.yml restart
   ```

### Code Style
- **Python**: PEP 8 compliance
- **JavaScript**: ES6+ features
- **CSS**: BEM methodology
- **Git**: Conventional commits

---

## 🔧 Troubleshooting

### Common Issues

#### Rankings not updating
```bash
# Force refresh
python management/force_refresh.py "City Name"

# Check data age
python management/check_data_age.py "City Name"
```

#### AI analysis missing
```bash
# Check AI quota
# Verify OpenAI API key
# Re-run analysis
python update_ai_analysis.py "City Name" --limit 5
```

#### Server errors
```bash
# Check Docker status
docker ps

# View error logs
docker logs kebab-rank-app --tail 100

# Restart everything
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

### API Limits
- **Google Places**: 
  - Solution: Implement caching, reduce update frequency
- **OpenAI**: 
  - Solution: Batch processing, use GPT-3.5-turbo
- **Supabase**: 
  - Solution: Optimize queries, clean old data

---

## 📈 Future Enhancements

### Planned Features
1. **User Reviews**: Allow users to add their own reviews
2. **Photo Gallery**: Kebab photos from Google/users
3. **Mobile App**: React Native application
4. **Advanced Filters**: Price range, halal, delivery
5. **Business Dashboard**: For restaurant owners

### Technical Improvements
1. **GraphQL API**: Better data fetching
2. **Redis Cache**: Faster response times
3. **Elasticsearch**: Full-text search
4. **ML Pipeline**: Custom models for Polish NLP
5. **Real-time Updates**: WebSocket integration

---

## 📝 License

All rights reserved © 2024 kebabrank.com

---

## 🤝 Contributing

This is currently a private project. For inquiries about collaboration or licensing, please contact the owner.

---

## 📞 Contact

- **Website**: [kebabrank.com](https://kebabrank.com)
- **Email**: kebabrank@gmail.com
- **Instagram**: [@kebabrank](https://instagram.com/kebabrank)
- **TikTok**: [@kebabrank](https://tiktok.com/@kebabrank)

---

Made with ❤️ and 🥙 in Poland