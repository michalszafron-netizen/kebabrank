# Kebab App Update Guide

This guide explains how to use the "elastic" update scripts to refresh data and AI analysis.
r
Open Editor
Workspaces
Antigravity1

kebsioronredesign

kebsioronredesign.code-workspace

manyprojects.code-workspace

Maaza

projekt1

Testy

WordpressDesign

Playground

kebsioronredesign
/
Refining Kebab Qualification

## 1. Master Update Script: `run_updates.py`
This is your primary tool. It coordinates GMaps ranking updates (with trend arrows) and AI analysis in one go.

### Update Single City
```powershell
python run_updates.py --city Tychy
```

### Update Multiple Cities (Batch)
```powershell
python run_updates.py --city Tychy Zakopane Warsaw
```

### Update ALL Cities in Database
```powershell
python run_updates.py --all
```

### Adjusting AI Limit
By default, it analyzes the top 5 places per city. You can change this:
```powershell
python run_updates.py --city Tychy --limit 10
```

### Skip AI Analysis
If you only want to update Rankings/Arrows quickly without using AI tokens:
```powershell
python run_updates.py --city Tychy --no-ai
```

---

## 2. Individual Scripts (Internal)
While `run_updates.py` is recommended, you can still use the individual components:

### `update_city_gmaps.py`
Updates list of places, ratings, and calculates rank trends (up/down/NEW).
```powershell
python update_city_gmaps.py "City Name"
```

### `update_city_review_ai.py`
Runs DeepSeek analysis on the latest reviews from Serper.dev.
```powershell
python update_city_review_ai.py "City Name" --limit 5
```

---

## 3. Verification Scripts
To quickly check results in your terminal:
```powershell
python verify_ai.py Tychy
```
