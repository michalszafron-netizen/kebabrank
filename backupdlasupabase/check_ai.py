import os

SQL_FILE = r'C:\Users\markowyy\Documents\kebsioronredesign\backups\supabase_dump_20260226_144452.sql'

def check_ai_analysis():
    with open(SQL_FILE, 'rb') as f:
        content = f.read()
    
    if b'COPY "public"."ai_analysis"' in content:
        print("FOUND: ai_analysis")
    else:
        print("NOT FOUND: ai_analysis")

if __name__ == "__main__":
    check_ai_analysis()
