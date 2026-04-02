import os
from dotenv import load_dotenv
from services.pocketbase_db import PocketbaseService

load_dotenv()
pb = PocketbaseService(os.getenv('PB_URL'))
city_id = pb.get_city_id('Kraków')
records = pb.client.collection('ratings').get_full_list(
    query_params={
        'filter': f'kebab_place.city="{city_id}"',
        'sort': '-created',
        'expand': 'kebab_place'
    }
)

aladdin = [r for r in records if r.expand['kebab_place'].name == 'Aladdin Shawarma & Falafel']
if aladdin:
    p = aladdin[0].expand['kebab_place']
    print(f"Place ID: {p.id}")
    print(f"Place Created: {p.created}")
    print(f"Place Type of Created: {type(p.created)}")
