# 🥙 Kebab Rank Poland

Find the best kebabs in Poland based on Google ratings!

## 🌟 Features

- Search kebabs in 50+ Polish cities
- Rankings based on Google ratings and review count
- Data refreshed every 7 days
- Global Top 10 kebabs across Poland
- Mobile-friendly design

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Database**: Supabase
- **API**: Google Places API
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Docker-ready

## 🚀 Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kebab-rank.git
cd kebab-rank
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create `.env` file with:
```
GOOGLE_API_KEY=your_google_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
ADMIN_KEY=your_admin_key
```

5. Set up database:
- Create Supabase project
- Run SQL schema from `database/schema.sql`

6. Run the application:
```bash
python app.py
```

## 📊 Ranking Algorithm

- **85%** - Google star rating
- **15%** - Review count (logarithmic scale)

## 🏆 Top Features Coming Soon

- User reviews
- Photo gallery
- "Near me" functionality
- Restaurant owner claims

## 📝 License

All rights reserved © 2024 kebabrank.com

## 🤝 Contributing

This is a private project. For suggestions, please contact the owner.

---
Made with ❤️ and 🥙 in Poland
