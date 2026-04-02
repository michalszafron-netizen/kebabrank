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

# Fetch the OpenAPI spec which contains the list of tables
response = requests.get(f"{SUPABASE_URL}/rest/v1/?apikey={SUPABASE_KEY}", headers=headers)

if response.status_code == 200:
    spec = response.json()
    tables = spec.get('definitions', {})
    print(f"Found {len(tables)} definitions/tables.")
    
    for table_name, details in tables.items():
        print(f"\n--- Table: {table_name} ---")
        properties = details.get('properties', {})
        for col, col_details in properties.items():
            print(f"  {col}: {col_details.get('type')} ({col_details.get('format', '')})")
else:
    print(f"Failed to fetch schema. Status code: {response.status_code}")
    print(response.text)
