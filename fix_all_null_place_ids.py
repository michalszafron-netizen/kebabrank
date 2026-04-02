#!/usr/bin/env python3
"""
Manual fix script for NULL place_ids in ratings_history table.
This script will find and fix all NULL place_id ratings in the database.
Uses proper table joins since ratings_history doesn't have google_place_id column.
"""

import os
from dotenv import load_dotenv
from services.database import DatabaseService

def fix_all_null_place_ids():
    """Find and fix all NULL place_id ratings in the database"""
    load_dotenv()
    
    # Initialize database service
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing SUPABASE_URL or SUPABASE_KEY in .env file")
        return
    
    db_service = DatabaseService(supabase_url, supabase_key)
    
    print("🔍 Searching for NULL place_id ratings...")
    
    try:
        # Find all ratings with NULL place_id
        null_ratings_response = db_service.client.table('ratings_history').select(
            'id'
        ).is_('kebab_place_id', 'null').execute()
        
        if not null_ratings_response.data:
            print("✅ No NULL place_id ratings found!")
            return
        
        print(f"⚠️  Found {len(null_ratings_response.data)} NULL place_id ratings")
        print("This approach cannot fix these ratings because:")
        print("- ratings_history table has no google_place_id column")
        print("- Cannot determine which kebab place these ratings belong to")
        print("- The data relationship is broken")
        
        print(f"\n📊 Summary: {len(null_ratings_response.data)} ratings have NULL place_id")
        print("💡 These ratings cannot be automatically fixed and should be deleted")
        print("   They represent broken data relationships")
        
        # Ask user if they want to delete these broken records
        response = input("\n❓ Do you want to DELETE these broken ratings? (y/N): ")
        if response.lower() == 'y':
            delete_count = 0
            for rating in null_ratings_response.data:
                try:
                    db_service.client.table('ratings_history').delete().eq('id', rating['id']).execute()
                    delete_count += 1
                    print(f"🗑️  Deleted rating {rating['id']}")
                except Exception as e:
                    print(f"❌ Error deleting rating {rating['id']}: {e}")
            
            print(f"\n🎯 Deletion Summary:")
            print(f"🗑️  Deleted: {delete_count} broken ratings")
            print(f"📊 Total processed: {len(null_ratings_response.data)} ratings")
            
            if delete_count > 0:
                print("\n🎉 Successfully cleaned up broken ratings!")
                print("💡 Run your update script again to create fresh, properly linked ratings")
            else:
                print("\n⚠️  No ratings were deleted.")
        else:
            print("\n⚠️  Keeping broken ratings. They will continue to cause issues.")
            
    except Exception as e:
        print(f"❌ Error searching for NULL place_id ratings: {e}")

def alternative_fix_approach():
    """Alternative approach: Fix NULL place_ids by matching on other criteria"""
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing SUPABASE_URL or SUPABASE_KEY in .env file")
        return
    
    db_service = DatabaseService(supabase_url, supabase_key)
    
    print("\n🔄 Alternative approach: Checking for fixable NULL place_ids...")
    
    # This is a more complex approach that would require additional data
    # to match NULL ratings to their proper kebab places
    print("⚠️  Complex matching approach not implemented")
    print("💡 The automatic fix in database.py should handle future NULL place_ids")

if __name__ == "__main__":
    fix_all_null_place_ids()
