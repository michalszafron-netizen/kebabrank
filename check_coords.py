import os
import sys
import io
import requests
from dotenv import load_dotenv
from pocketbase import PocketBase

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()
pb = PocketBase(os.getenv('PB_URL'))
pb.admins.auth_with_password(os.getenv('PB_EMAIL'), os.getenv('PB_PASSWORD'))

city = pb.collection('cities').get_first_list_item('name="Zakopane"')
print(f"City: {city.name} | Lat: {getattr(city, 'lat', 'N/A')} | Lng: {getattr(city, 'lng', 'N/A')}")
# If no lat/lng, check a place in that city
place = pb.collection('kebab_places').get_first_list_item(f'city="{city.id}"')
if place:
    print(f"Sample Place: {place.name} | Lat: {place.lat} | Lng: {place.lng}")
