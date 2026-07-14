import requests
import json
import os
from dotenv import load_dotenv

load_dotenv('c:\\Users\\markowyy\\Documents\\kebsioronredesign\\.env')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}'
}

# Fetch sample from kebab_places
response = requests.get(f"{SUPABASE_URL}/rest/v1/kebab_places?select=id,name,photo_url&limit=3", headers=headers)

if response.status_code == 200:
    for row in response.json():
        print(f"ID: {row['id']} | Name: {row['name']} | Photo URL: {row['photo_url']}")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
