# Kebab Ranking Application - Command Reference

## 📋 Quick Start & Overview

### Prerequisites
- Python 3.8+
- Supabase database credentials in `.env` file
- Google Places API key in `.env` file

### Essential Environment Variables
```bash
# .env file should contain:
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GOOGLE_API_KEY=your_google_api_key
```

### Basic Navigation
```bash
# Navigate to project directory
cd kebab-rank

# Activate virtual environment (if using)
python -m venv venv
venv\Scripts\activate  # Windows
```

---

## 🔄 Data Collection & Updates

### 1. Update All Cities (Bulk Update)
**Purpose**: Fetch fresh kebab data for all 62 cities from Google Places API

```bash
# Update all cities at once
python update_all_cities.py

# Expected output: Progress through all 62 cities with success/failure status
```

**Parameters**: None - runs full update for all cities

**Frequency**: Weekly or monthly for fresh data

### 2. Update AI Analysis
**Purpose**: Generate AI-enhanced scores and analysis for kebabs

```bash
# Update AI analysis for all kebabs
python update_ai_analysis.py

# Update specific city only
python update_ai_analysis.py --city Warszawa
```

**Parameters**:
- `--city CITY_NAME`: Process specific city only
- `--limit N`: Limit number of kebabs processed

**Frequency**: After major data updates

### 3. Test Google Places API
**Purpose**: Verify Google API connectivity and test city searches

```bash
# Test basic API connectivity
python test_google.py

# Test specific city search
python test_google.py --city Kraków
```

**Use Case**: Debugging API issues or testing new city searches

---

## 🛠️ Data Quality & Maintenance

### 4. Check City Mixing Issues
**Purpose**: Detect kebabs assigned to wrong cities based on postal codes

```bash
# Comprehensive analysis of all cities
python check_all_city_mixing.py
```

**Output**: Detailed report showing:
- Cities with misassignments
- Number of issues per city
- Postal code mismatches
- Severity levels

**Frequency**: After major data updates or when noticing incorrect city assignments

### 5. Fix City Mixing Issues
**Purpose**: Automatically correct misassigned kebabs

```bash
# Fix all identified issues (requires confirmation)
python fix_all_city_mixing.py
```

**Safety**: Asks for confirmation before making database changes

**Frequency**: Run after `check_all_city_mixing.py` identifies issues

### 6. Fix Pszczyna-Specific Issues
**Purpose**: Targeted fix for Kraków kebabs incorrectly in Pszczyna

```bash
# Fix Pszczyna misassignments only
python fix_pszczyna_misassignments.py
```

**Use Case**: When specific city has known mixing issues

### 7. Create Historical Data
**Purpose**: Generate realistic historical ranking data for badge system

```bash
# Preview changes for specific city
python create_historical_data.py --city Warszawa --preview

# Apply changes for specific city
python create_historical_data.py --city Warszawa --apply --backup

# Apply for all cities
python create_historical_data.py --all-cities --apply --backup
```

**Parameters**:
- `--city CITY_NAME`: Process specific city
- `--all-cities`: Process all cities
- `--preview`: Show changes without applying
- `--apply`: Apply changes to database
- `--backup`: Create backup before changes
- `--validate`: Verify changes after applying

**Use Case**: When ranking badges show "NEW" for all kebabs (no historical data)

---

## 🧪 Testing & Debugging

### 8. Test Ranking System
**Purpose**: Verify ranking algorithm and badge system

```bash
# Test ranking functionality
python test_badges.py

# Test specific city rankings
python -c "from services.database import DatabaseService; db = DatabaseService(); rankings = db.get_city_rankings('Warszawa', limit=5); print([r['name'] for r in rankings])"
```

### 9. Test Database Connection
**Purpose**: Verify Supabase connectivity

```bash
# Quick database test
python test_env_loading.py

# Test specific database operations
python simple_test.py
```

### 10. Test City Mapping
**Purpose**: Verify city name consistency

```bash
# Check city name mappings
python test_city_mapping.py

# Detect all city mixing patterns
python detect_all_city_mixing.py
```

---

## 🌐 Website Management

### 11. Run Flask Application
**Purpose**: Start the web interface

```bash
# Start development server
python app.py

# Or using Flask directly
flask run

# Access at: http://localhost:5000
```

### 12. Test Frontend Functionality
**Purpose**: Verify search and ranking display

1. Open browser to `http://localhost:5000`
2. Test city search functionality
3. Verify ranking badges (up/down arrows, NEW indicators)
4. Check countdown timer functionality

---

## 🔧 Maintenance Workflows

### Weekly Maintenance Routine
```bash
# 1. Update all cities with fresh data
python update_all_cities.py

# 2. Update AI analysis
python update_ai_analysis.py

# 3. Check for data quality issues
python check_all_city_mixing.py

# 4. Fix any identified issues (if needed)
python fix_all_city_mixing.py

# 5. Verify website functionality
# Start server and test manually
```

### Monthly Deep Clean
```bash
# 1. Comprehensive data quality check
python check_all_city_mixing.py

# 2. Generate fresh historical data if needed
python create_historical_data.py --all-cities --apply --backup

# 3. Full AI analysis update
python update_ai_analysis.py --all

# 4. Database optimization (if needed)
# Check Supabase dashboard for performance metrics
```

### Troubleshooting Common Issues

#### Issue: All badges show "NEW"
**Solution**: Generate historical data
```bash
python create_historical_data.py --all-cities --apply --backup
```

#### Issue: City search not working
**Solution**: Check JavaScript console for errors, verify API endpoints

#### Issue: Incorrect kebabs in city listings
**Solution**: Run city mixing detection and fix
```bash
python check_all_city_mixing.py
python fix_all_city_mixing.py
```

#### Issue: Google API errors
**Solution**: Test API connectivity
```bash
python test_google.py
# Check GOOGLE_API_KEY in .env file
```

---

## 📊 Monitoring & Best Practices

### Data Quality Indicators
- **Good**: Ranking badges show proper up/down arrows
- **Good**: City searches return relevant results
- **Warning**: Many "NEW" badges indicate missing historical data
- **Critical**: Kebabs from wrong cities appearing in listings

### Performance Tips
- Run bulk updates during off-peak hours
- Monitor Google API usage limits
- Regular database backups via Supabase dashboard
- Test individual cities before full updates

### Safety Notes
- Always use `--preview` before `--apply` for destructive operations
- Keep `.env` file secure with API keys
- Regular database backups are essential
- Test changes on staging environment first if available

---

## 🆘 Emergency Procedures

### Database Recovery
If major data corruption occurs:
1. Restore from Supabase backup
2. Run `python create_historical_data.py --all-cities --apply --backup` to regenerate rankings
3. Verify data integrity with `python check_all_city_mixing.py`

### API Key Issues
If Google API stops working:
1. Verify API key in `.env` file
2. Check Google Cloud Console for quota limits
3. Test with `python test_google.py`

### Website Not Loading
1. Check if Flask server is running: `python app.py`
2. Verify port 5000 is available
3. Check browser console for JavaScript errors

---

## 📞 Support & Resources

### Key Files Location
- **Main application**: `app.py`
- **Database service**: `services/database.py`
- **Google Places**: `services/google_places.py`
- **Ranking logic**: `services/ranking.py`
- **Frontend**: `static/js/app.js`, `templates/index.html`

### Environment Setup
Ensure these Python packages are installed:
```bash
pip install flask python-dotenv googlemaps supabase
```

### Log Files
- Check terminal output for script execution logs
- Browser developer console for frontend issues
- Supabase dashboard for database query logs

---

*Last Updated: September 2025*  
*Maintained by: Kebab Ranking System*
