import os
import time
import requests
from services.database import DatabaseService

def apply_migration():
    # Initialize database connection
    db = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    
    # Read the SQL migration file
    with open('migrations/202507101207_add_city_rankings_function.sql', 'r') as f:
        sql = f.read()
    
    try:
        print("Attempting to apply migration via SQL API...")
        # Use Supabase's SQL endpoint directly
        url = f"{os.getenv('SUPABASE_URL')}/rest/v1/sql"
        headers = {
            'apikey': os.getenv('SUPABASE_KEY'),
            'Authorization': f"Bearer {os.getenv('SUPABASE_KEY')}",
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json={'query': sql})
        
        if response.status_code == 200:
            print("Migration submitted successfully. Waiting for function to be available...")
            
            # Wait and verify function exists
            max_attempts = 5
            for attempt in range(max_attempts):
                time.sleep(2)
                try:
                    test_result = db.client.rpc('get_city_rankings_with_latest_ratings', 
                                              {'p_city_id': 1, 'p_limit': 1, 'p_offset': 0}).execute()
                    print("Function verified successfully!")
                    return True
                except Exception as e:
                    if attempt == max_attempts - 1:
                        print(f"Verification failed after {max_attempts} attempts. Error:", e)
                        return False
                    print(f"Verification attempt {attempt + 1} failed, retrying...")
        else:
            print(f"Migration failed with status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print("Error applying migration:", e)
        return False

if __name__ == "__main__":
    apply_migration()
