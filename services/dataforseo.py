import time
import requests
from typing import List, Dict
from requests.exceptions import RequestException

class DataForSEOService:
    BASE = "https://api.dataforseo.com/v3"
    TASK_TIMEOUT = 120  # seconds

    def __init__(self, login: str, password: str):
        self.auth = (login, password)

    def _post(self, path: str, payload: list) -> dict:
        r = requests.post(f"{self.BASE}{path}", auth=self.auth, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()

    def _get(self, path: str) -> dict:
        r = requests.get(f"{self.BASE}{path}", auth=self.auth, timeout=30)
        r.raise_for_status()
        return r.json()

    def search_places(self, query: str, depth: int = 100) -> List[Dict]:
        """
        Search Google Maps via DataForSEO SERP Maps endpoint.
        depth: number of results to fetch (default 100, up to 700 for large cities).
        """
        try:
            data = self._post("/serp/google/maps/task_post", [{
                "keyword": query,
                "location_name": "Poland",
                "language_name": "Polish",
                "language_code": "pl",
                "depth": depth,
            }])
        except RequestException as e:
            print(f"  DataForSEO API error (task_post): {e}")
            return []

        t = (data.get('tasks') or [{}])[0]
        task_id = t.get('id')
        cost = t.get('cost', 0)
        if not task_id:
            print(f"  DataForSEO: task creation failed — {t.get('status_message')}")
            return []
        print(f"  Task {task_id} (${cost:.5f})")

        # Poll tasks_ready
        deadline = self.TASK_TIMEOUT // 5
        for attempt in range(deadline):
            time.sleep(5)
            try:
                ready_data = self._get("/serp/google/maps/tasks_ready")
                ready_ids = [
                    x.get('id') for x in
                    ((ready_data.get('tasks') or [{}])[0].get('result') or [])
                ]
                if task_id in ready_ids:
                    break
            except RequestException:
                pass
            if attempt % 6 == 5:
                print(f"  Still waiting... ({(attempt + 1) * 5}s)")
        else:
            print(f"  DataForSEO: task {task_id} not ready after {self.TASK_TIMEOUT}s — trying anyway")

        try:
            result_data = self._get(f"/serp/google/maps/task_get/advanced/{task_id}")
        except RequestException as e:
            print(f"  DataForSEO API error (task_get): {e}")
            return []

        rt = (result_data.get('tasks') or [{}])[0]
        if rt.get('status_code') != 20000:
            print(f"  DataForSEO task_get: {rt.get('status_code')} - {rt.get('status_message')}")
            return []

        result = (rt.get('result') or [{}])[0]
        items = result.get('items') or []
        print(f"  Got {len(items)} items from DataForSEO")
        return items

    def check_businesses_status(self, places: list) -> dict:
        """
        Batch-check business status via my_business_info for a list of places.
        places: [{'google_place_id': str, 'name': str, 'city': str}, ...]
        Returns: {google_place_id: 'temporarily_closed'|'permanently_closed'|'operational'}

        Status is in: result[0]['items'][0]['work_time']['work_hours']['current_status']
        Values: 'open', 'closed', 'temporarily_closed', 'permanently_closed'
        """
        if not places:
            return {}

        payload = [
            {
                "keyword": f"{p['name']} {p['city']}",
                "location_name": "Poland",
                "language_name": "Polish",
                "language_code": "pl",
            }
            for p in places
        ]

        try:
            data = self._post("/business_data/google/my_business_info/task_post", payload)
        except RequestException as e:
            print(f"  check_businesses_status error (task_post): {e}")
            return {}

        tasks = data.get('tasks') or []
        place_ids = [p['google_place_id'] for p in places]

        # Map task_id -> place_id by index order (DataForSEO preserves order)
        task_id_map = []
        total_cost = 0
        for i, t in enumerate(tasks):
            tid = t.get('id')
            cost = t.get('cost', 0)
            total_cost += cost
            if tid and i < len(place_ids):
                task_id_map.append((tid, place_ids[i]))

        if not task_id_map:
            return {}

        print(f"  Status check: {len(task_id_map)} tasks created (${total_cost:.5f})")

        # Poll tasks_ready until all done (they run in parallel on DataForSEO side)
        remaining = {tid for tid, _ in task_id_map}
        for attempt in range(30):  # max 150s
            time.sleep(5)
            try:
                ready_data = self._get("/business_data/google/my_business_info/tasks_ready")
                ready_ids = {
                    x.get('id') for x in
                    ((ready_data.get('tasks') or [{}])[0].get('result') or [])
                }
                remaining -= ready_ids
            except RequestException:
                pass
            if not remaining:
                break
            if attempt % 6 == 5:
                print(f"  Still waiting for {len(remaining)} tasks... ({(attempt + 1) * 5}s)")

        # Fetch all results
        status_map = {}
        for task_id, place_id in task_id_map:
            try:
                result_data = self._get(f"/business_data/google/my_business_info/task_get/{task_id}")
                rt = (result_data.get('tasks') or [{}])[0]
                if rt.get('status_code') != 20000:
                    continue
                outer = (rt.get('result') or [{}])[0]
                items = outer.get('items') or []
                if not items:
                    continue
                item = items[0]
                work_time = item.get('work_time') or {}
                work_hours = work_time.get('work_hours') or {}
                status = work_hours.get('current_status') or 'operational'
                status_map[place_id] = status
            except Exception as e:
                print(f"  Error fetching status for task {task_id}: {e}")

        return status_map
