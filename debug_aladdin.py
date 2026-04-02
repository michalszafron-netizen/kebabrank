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
for r in aladdin:
    print(f'Created: {r.created}, Score: {getattr(r, "rank_score", 0)}, City Rank: {getattr(r, "city_rank", 0)}')
