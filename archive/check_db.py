import os
from dotenv import load_dotenv
load_dotenv()
from services.pocketbase_db import PocketbaseService
pb = PocketbaseService(os.environ.get("PB_URL"))
pb._ensure_auth()
try:
    p = pb.client.collection("kebab_places").get_first_list_item("name='ARABIAN KING KEBAB'")
    print(dir(p))
    if hasattr(p, 'collection_id'):
        print(f"collection_id: {p.collection_id}")
    print(f"vars: {vars(p)}")
except Exception as e:
    print(e)
