# generate_sitemap.py

import os
from dotenv import load_dotenv
from services.database import DatabaseService

load_dotenv()

BASE_URL = "https://kebabrank.com"

def slugify(name):
    return name.strip().lower().replace(" ", "-")

def generate_sitemap():
    db = DatabaseService(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    cities = db.get_cities()

    urls = [f"{BASE_URL}/"]
    # City pages
    for city in cities:
        slug = slugify(city['name'])
        urls.append(f"{BASE_URL}/kebab-{slug}")

    # Blog index and articles
    blog_slugs = ["", "najlepszy-kebab-krakow", "ranking-kebabow-warszawa", "najlepszy-kebab-szczecin", "najlepszy-kebab-lodz", "najlepszy-kebab-bydgoszcz", "najlepszy-kebab-lublin", "najlepszy-kebab-katowice", "najlepszy-kebab-wroclaw", "gdzie-na-kebaba"]
    for slug in blog_slugs:
        path = f"/blog/{slug}" if slug else "/blog"
        urls.append(f"{BASE_URL}{path}")

    # Legal
    urls.extend([f"{BASE_URL}/privacy", f"{BASE_URL}/terms"])

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap += f"  <url><loc>{url}</loc></url>\n"
    sitemap += '</urlset>'

    with open("static/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("✅ sitemap.xml generated at /static/sitemap.xml")

if __name__ == "__main__":
    generate_sitemap()
