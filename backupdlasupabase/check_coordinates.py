#!/usr/bin/env python3
"""
Script to check coordinate data in kebab_places table
"""

from services.database import DatabaseService
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    db = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

    # Check if kebab_places table has coordinates
    response = db.client.table('kebab_places').select('id, name, latitude, longitude').limit(5).execute()
    print('Sample kebab places with coordinates:')
    for place in response.data:
        print(f"{place['name']}: lat={place.get('latitude')}, lng={place.get('longitude')}")

    # Count places with and without coordinates
    with_coords = db.client.table('kebab_places').select('id').not_.is_('latitude', 'null').not_.is_('longitude', 'null').execute()
    without_coords = db.client.table('kebab_places').select('id').is_('latitude', 'null').is_('longitude', 'null').execute()

    print(f'\nPlaces with coordinates: {len(with_coords.data)}')
    print(f'Places without coordinates: {len(without_coords.data)}')

if __name__ == '__main__':
    main()
