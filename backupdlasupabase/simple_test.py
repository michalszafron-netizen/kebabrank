#!/usr/bin/env python3
"""Simple test to check if the script can run"""

import os
import sys

# Test environment loading
def load_env_file():
    """Simple .env file loader"""
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("✓ Loaded environment variables from .env file")
        return True
    except FileNotFoundError:
        print("⚠ .env file not found")
        return False
    except Exception as e:
        print(f"⚠ Error loading .env file: {e}")
        return False

print("=== SIMPLE TEST ===")
load_env_file()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

print(f"SUPABASE_URL: {supabase_url[:20]}..." if supabase_url else "MISSING")
print(f"SUPABASE_KEY: {supabase_key[:20]}..." if supabase_key else "MISSING")

if supabase_url and supabase_key:
    print("✓ Environment variables loaded successfully!")
    print("The script should work now.")
else:
    print("✗ Environment variables are missing")
