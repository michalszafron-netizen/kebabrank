# 🥙 KebabRank Poland - AI-Powered Kebab Ranking Platform

[![Website](https://img.shields.io/badge/Website-kebabrank.com-orange)](https://kebabrank.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green)](https://flask.palletsprojects.com/)
[![PocketBase](https://img.shields.io/badge/Database-PocketBase-blue)](https://pocketbase.io)
[![Update Logic](https://img.shields.io/badge/Search-GmapsExtractor-orange)](https://cloud.gmapsextractor.com)

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Features](#features)
5. [Project Structure](#project-structure)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [Database Schema (PocketBase)](#database-schema-pocketbase)
9. [Scoring & Ranking Logic](#scoring--ranking-logic)
10. [AI Integration](#ai-integration)
11. [Admin Management](#admin-management)
12. [Deployment](#deployment)
13. [Monitoring & Maintenance](#monitoring--maintenance)
14. [Troubleshooting](#troubleshooting)

---

## 🌟 Overview

KebabRank is Poland's first AI-powered kebab ranking platform that combines real-time Google Maps data with advanced sentiment analysis to provide the most comprehensive kebab rankings across Polish cities. 

The platform utilizes a **Three-Pillar Stability System**:
1. **Smart Filtering**: Regex-based address verification to eliminate "ghost entries" from neighboring cities.
2. **Batch-Aware Trends**: Persistent historical ranking records that ensure trend arrows (up/down/neutral) are accurate even after multiple updates per day.
3. **Sentiment Analysis**: Machine learning models (OpenAI) that analyze customer emotions and detect fake review patterns.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                              │
│         Vanilla JS + Responsive CSS + PocketBase SDK          │
└─────────────────────┬───────────────────────────────────────┘
                      │ (Real-time data sync)
┌─────────────────────▼───────────────────────────────────────┐
│                    Flask Backend                              │
│          API Routes + Ranking Logic + AI Processing           │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┬─────────────────────┐
        │                           │                      │
┌───────▼────────┐          ┌──────▼──────┐      ┌───────▼────────┐
│ Gmapsextractor │          │  PocketBase  │      │   OpenAI API   │
│   (Serper)     │          │  (SQLite)    │      │ (GPT-3.5/GPT-4)│
└────────────────┘          └─────────────┘      └────────────────┘
```

---

## 💻 Technology Stack

### Backend
- **Framework**: Flask 2.3.3 (Python 3.10+)
- **WSGI Server**: Gunicorn (production)
- **Database**: **PocketBase** High-performance Go-based backend (SQLite engine)
- **API Integration**: 
  - **GmapsExtractor**: High-speed Google Maps scraping and structured data extraction.
  - **Serper.dev**: Failover API for detailed place reviews and images.
  - **OpenAI**: Advanced sentiment analysis and AI-generated Polish summaries.

### Frontend
- **Core**: Vanilla JavaScript (ES6+) with direct PocketBase SDK integration.
- **Styling**: Premium CSS with Flexbox/Grid and Glassmorphism effects.
- **Dynamic UI**: Real-time trend indicators (arrows), medals for TOP 3, and status badges.

---

## ✨ Features

### Core Features
1. **Dynamic City Rankings**: Real-time rankings for over 50+ Polish cities.
2. **Smart City Filter (The "Goat" Killer)**: Uses regex postal code verification (`XX-XXX City`) to ensure places in neighbor cities don't pollute the local ranking.
3. **Ghost Elimination**: Automated cleanup process that hides establishments no longer found in the latest search.
4. **Historical Persistence**: Every update cycle creates a timestamped record, allowing for year-long quality tracking.

### AI-Powered Intelligence
1. **Sentiment Index**: Calculation of customer happiness based on review text analysis.
2. **Fake Review Filter**: Pattern matching to adjust scores of places with suspicious activity.
3. **AI Summary**: Automatically generated, human-like summaries of what customers love and hate about a place.

---

## 📁 Project Structure

```
kebab-rank/
├── app.py                    # Flask application & SEO Routing
├── update_city_gmaps.py      # Main Data Update Entry Point
├── requirements.txt          # Python dependencies
├── .env                      # API Keys (PocketBase, OpenAI, GmapsExtractor)
│
├── services/                 # Core Logic Layer
│   ├── pocketbase_db.py      # PocketBase abstraction with trend preservation
│   ├── gmaps_extractor.py    # GmapsExtractor (Cloud) integration
│   ├── ranking.py            # The 85/15 Scoring Algorithm
│   ├── ai_service.py         # OpenAI sentiment logic
│   └── ai_data_updater.py    # Batch AI processing
│
├── templates/               # SEO-Optimized HTML Templates
│   ├── index.html           # Main SPA entry
│   ├── city_detail.html     # SEO-specific city pages
│   └── blog/                # Content-driven blog posts
│
├── static/                  # Production Assets
│   ├── js/app.js            # Main frontend logic (Socket-like updates)
│   └── css/style.css        # Premium UI styles
│
└── management/              # Operational Scripts
    ├── restart_flask_clean.py # Cache clearing & server restart
    └── generate_sitemap.py  # Automated SEO maintenance
```

---

## 🚀 Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kebab-rank.git
   cd kebab-rank
   ```

2. **PocketBase Server**
   - Download the [PocketBase binary](https://pocketbase.io/docs/).
   - Run `./pocketbase serve` locally.
   - Access admin panel at `http://localhost:8090/_/`.

3. **Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

4. **Environment Configuration (`.env`)**
   ```env
   PB_URL=http://localhost:8090
   PB_EMAIL=admin@kebabrank.com
   PB_PASSWORD=your_secure_password
   GMAPS_API_KEY=your_gmapsextractor_key
   OPENAI_API_KEY=your_openai_key
   ```

---

## 📊 Scoring & Ranking Logic

### The 85/15 Formula
To ensure that rankings aren't manipulated by a few 5-star fake reviews, we use a weighted reliability model:

- **85% - Raw Rating Score**: Linear normalization of the 0-5 star Google rating.
- **15% - Review Reliability**: A logarithmic scale based on the total number of reviews.
  - *Formula*: `min(log10(reviews + 1) / 3 * 100, 100) * 0.15`
  - *Effect*: A 4.9 rating based on 500 reviews will outrank a 5.0 rating based on 2 reviews.

---

## 👨‍💼 Admin Management

### Updating a City
To trigger a fresh update for a city (e.g., Chorzów), run:
```bash
python update_city_gmaps.py "Chorzów"
```
*This script will:*
1. **Reset**: Create `0-rank` placeholders for old entries (Ghost Elimination).
2. **Fetch**: Extract 5 pages of results from GmapsExtractor.
3. **Filter**: Discard results with wrong postal codes.
4. **Rank**: Calculate scores and compare against historical timestamps for Trend Arrows.
5. **Save**: Persist new rating records to PocketBase.

### Refreshing the Website Cache
If you see old data on the live site after an update:
```bash
python restart_flask_clean.py
```

---

## 🚢 Deployment (Hostinger VPS)

Our production environment uses **Docker Compose** behind an **Nginx** reverse proxy.

### Quick Deploy
```bash
# Pull latest changes
git pull

# Rebuild containers
docker-compose -f docker-compose.prod.yml up -d --build

# Verify logs
docker logs -f kebabrank_app
```

---

## 🔧 Troubleshooting

- **Trend Arrows are all neutral (-)**: 
  - Ensure you have at least two separate timestamped updates for the city. 
  - The system needs a "before" and "after" record to calculate change.
- **"Ghost" places from other cities appearing**: 
  - Check the city name spelling in `update_city_gmaps.py`. 
  - The regex postal code filter relies on the address provided by Google Maps.
- **PocketBase Connection Errors**: 
  - Verify your `PB_URL` in `.env` includes the protocol (e.g., `https://` vs `http://`).

---

Made with ❤️ and 🥙 in Poland.
© 2026 kebabrank.com | All rights reserved.