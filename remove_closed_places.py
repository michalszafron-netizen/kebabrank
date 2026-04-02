# remove_closed_places.py - Script to remove permanently closed kebab places from the database
import os
import argparse
from dotenv import load_dotenv
from services.database import DatabaseService
from services.google_places import GooglePlacesService

# Load environment variables
load_dotenv()

def main():
    """
    Main function to find and remove permanently closed kebab places.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Remove permanently closed kebab places from the database.")
    parser.add_argument('city_name', nargs='?', default=None, help="Optional: Specify a single city to process (e.g., 'Pszczyna'). If not provided, processes all cities.")
    args = parser.parse_args()

    target_city = args.city_name

    print("🧹 Starting cleanup of permanently closed kebab places...")
    if target_city:
        print(f"📍 Targeting city: {target_city}")
    else:
        print("📍 Targeting all cities")
    print("=" * 60)

    # Initialize services
    db_service = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    google_service = GooglePlacesService(os.getenv('GOOGLE_API_KEY'))

    # Get kebab places from the database
    if target_city:
        print(f"Fetching kebab places for '{target_city}' from the database...")
    else:
        print("Fetching all kebab places from the database...")
    
    try:
        if target_city:
            # Fetch places for a specific city by joining with the cities table
            response = db_service.client.table('kebab_places').select(
                'id, name, google_place_id, cities!inner(name)'
            ).eq('cities.name', target_city).execute()
        else:
            # Fetch all places
            response = db_service.client.table('kebab_places').select('id, name, google_place_id').execute()
        
        all_places = response.data
    except Exception as e:
        print(f"❌ Error fetching kebab places from database: {e}")
        return

    if not all_places:
        if target_city:
            print(f"No kebab places found for '{target_city}' in the database. Exiting.")
        else:
            print("No kebab places found in the database. Exiting.")
        return

    if target_city:
        print(f"Found {len(all_places)} kebab places to check for '{target_city}'.")
    else:
        print(f"Found {len(all_places)} kebab places to check.")

    removed_count = 0
    error_count = 0

    for place in all_places:
        place_id = place['id']
        place_name = place['name']
        google_place_id = place['google_place_id']

        if not google_place_id:
            print(f"  ⚠️  Skipping place '{place_name}' (ID: {place_id}) - no google_place_id found.")
            continue

        print(f"\n🔍 Checking '{place_name}' (Google ID: {google_place_id})...")

        try:
            # Get current details from Google Places API
            # We need a method to get details by place_id and check business_status
            # The _get_place_details method in GooglePlacesService is almost what we need,
            # but it's designed for a specific city. Let's adapt its logic here.
            
            result = google_service.gmaps.place(
                place_id=google_place_id,
                fields=['name', 'business_status']
            )
            
            current_details = result.get('result', {})
            business_status = current_details.get('business_status')
            current_name = current_details.get('name', place_name) # Use current name if available

            if business_status == 'CLOSED_PERMANENTLY':
                print(f"  ❌ '{current_name}' is permanently closed. Removing from database...")
                try:
                    # Step 1: Delete all associated rating history first
                    print(f"     Deleting rating history for '{current_name}' (ID: {place_id})...")
                    db_service.client.table('ratings_history').delete().eq('kebab_place_id', place_id).execute()

                    # Step 2: Now, delete the kebab place itself
                    print(f"     Deleting kebab place '{current_name}' (ID: {place_id})...")
                    delete_response = db_service.client.table('kebab_places').delete().eq('id', place_id).execute()
                    
                    if delete_response.data: # Check if data was returned (indicating successful deletion)
                        print(f"     ✅ Successfully removed '{current_name}' and its history.")
                        removed_count += 1
                    else:
                        # This should ideally not happen if history deletion was successful
                        print(f"     ⚠️  Deletion of place '{current_name}' failed for an unknown reason after history was cleared.")
                        error_count += 1

                except Exception as delete_e:
                    print(f"     ❌ Error during deletion process for '{current_name}' (ID: {place_id}): {delete_e}")
                    error_count += 1
            else:
                status_display = business_status if business_status else 'OPERATIONAL (assumed)'
                print(f"  ✅ '{current_name}' is open or status is '{status_display}'. Keeping in database.")

        except Exception as e:
            error_message = str(e)
            print(f"  ❌ Error fetching details for '{place_name}' (Google ID: {google_place_id}) from Google API: {error_message}")
            
            # Check if the error is because the place was removed from Google
            if "NOT_FOUND" in error_message:
                print(f"     Place ID no longer exists on Google Maps. Assuming permanently closed. Removing from database...")
                try:
                    # Step 1: Delete all associated rating history first
                    print(f"     Deleting rating history for '{place_name}' (ID: {place_id})...")
                    db_service.client.table('ratings_history').delete().eq('kebab_place_id', place_id).execute()

                    # Step 2: Now, delete the kebab place itself
                    print(f"     Deleting kebab place '{place_name}' (ID: {place_id})...")
                    delete_response = db_service.client.table('kebab_places').delete().eq('id', place_id).execute()
                    
                    if delete_response.data:
                        print(f"     ✅ Successfully removed '{place_name}' and its history (Place ID was invalid).")
                        removed_count += 1
                    else:
                        print(f"     ⚠️  Deletion of place '{place_name}' failed for an unknown reason after history was cleared.")
                        error_count += 1
                except Exception as delete_e:
                    print(f"     ❌ Error during deletion process for '{place_name}' (ID: {place_id}): {delete_e}")
                    error_count += 1
            else:
                # For other types of errors, keep the old behavior
                print(f"     This is an unexpected error. Consider manual review or deletion.")
                error_count += 1
            
    print("\n" + "=" * 60)
    print("🎉 Cleanup process finished.")
    print(f"   Total places checked: {len(all_places)}")
    print(f"   Total places removed: {removed_count}")
    print(f"   Total errors encountered: {error_count}")
    print("\nIt's recommended to run 'fix_rankings_comprehensive.py' next to update rankings.")

if __name__ == "__main__":
    main()
