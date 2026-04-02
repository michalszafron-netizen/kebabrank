# generate_sitemap.py
import os
from dotenv import load_dotenv
from services.database import DatabaseService

load_dotenv()

BASE_URL = "https://www.kebabrank.com"

# ➊ blog slugs – keep in sync with app.py
BLOG_SLUGS = [
    "",                                 # /blog  (listing)
    "najlepszy-kebab-krakow",
    "ranking-kebabow-warszawa",
    "najlepszy-kebab-szczecin",
    "najlepszy-kebab-lodz",
    "najlepszy-kebab-bydgoszcz",
    "najlepszy-kebab-lublin",
    "najlepszy-kebab-katowice",
    "najlepszy-kebab-wroclaw",
    "gdzie-na-kebaba",
]

def slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "-")

def generate_sitemap() -> None:
    db = DatabaseService(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    cities = db.get_cities()

    urls = [f"{BASE_URL}/"]                  # homepage
    # ➋ add city pages (SEO optimized with kebab- prefix)
    urls += [f"{BASE_URL}/kebab-{slugify(c['name'])}" for c in cities]

    # ➌ add blog index and articles
    urls += [f"{BASE_URL}/blog{('/' + s) if s else ''}" for s in BLOG_SLUGS]

    # ➍ add legal pages
    urls += [f"{BASE_URL}/privacy", f"{BASE_URL}/terms"]

    # build XML
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{url}</loc></url>" for url in urls]
    sitemap.append('</urlset>')

    os.makedirs("static", exist_ok=True)
    with open("static/sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap))

    print(f"✅  sitemap.xml regenerated with {len(urls)} URLs")

if __name__ == "__main__":
    generate_sitemap()
