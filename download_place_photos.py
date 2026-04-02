import os
import requests
from dotenv import load_dotenv

load_dotenv('c:\\Users\\markowyy\\Documents\\kebsioronredesign\\.env')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}'
}

# Local folder to save the photos
# We will create directories for places
PHOTOS_DIR = "local_photos"
if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)

print("Fetching list of places and photos from Supabase...")

# We paginate over kebab_places just in case there are many
offset = 0
limit = 1000
all_places = []

while True:
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/kebab_places?select=id,name,photo_url&limit={limit}&offset={offset}",
        headers=headers
    )
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        print(response.text)
        break
        
    data = response.json()
    if not data:
        break
        
    all_places.extend(data)
    offset += limit
    
    if len(data) < limit:
        break

print(f"Total places retrieved: {len(all_places)}")

downloaded_count = 0
skipped_count = 0

for place in all_places:
    place_id = place['id']
    name = place.get('name', f"place_{place_id}")
    photo_url = place.get('photo_url')
    
    if not photo_url:
        continue
        
    # Clean the name to make it a safe filename
    safe_name = "".join([c if c.isalnum() else "_" for c in name])
    
    # Extract extension from URL if possible, otherwise default to .jpg
    ext = ".jpg"
    if photo_url.lower().endswith('.png'): ext = ".png"
    elif photo_url.lower().endswith('.jpeg'): ext = ".jpeg"
    elif photo_url.lower().endswith('.webp'): ext = ".webp"
    
    filename = f"{place_id}_{safe_name}{ext}"
    filepath = os.path.join(PHOTOS_DIR, filename)
    
    if os.path.exists(filepath):
        # File already downloaded
        skipped_count += 1
        continue
        
    # Ensure safe ascii printing for windows console
    safe_print_name = filename.encode('ascii', 'replace').decode('ascii')
    print(f"Downloading {safe_print_name}...")
    try:
        img_response = requests.get(photo_url, stream=True)
        if img_response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in img_response.iter_content(1024):
                    f.write(chunk)
            downloaded_count += 1
        else:
            print(f"  -> Failed to download: HTTP {img_response.status_code}")
    except Exception as e:
        print(f"  -> Exception while downloading: {e}")

print("\n--- Summary ---")
print(f"Newly downloaded: {downloaded_count}")
print(f"Skipped (already exists): {skipped_count}")
print(f"Photos are stored in: {os.path.abspath(PHOTOS_DIR)}")
