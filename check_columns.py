import os

SQL_FILE = r'C:\Users\markowyy\Documents\kebsioronredesign\backups\supabase_dump_20260226_144452.sql'

def check_columns():
    with open(SQL_FILE, 'rb') as f:
        content = f.read()
    
    pos = content.find(b'COPY "public"."ai_analysis"')
    if pos != -1:
        line_end = content.find(b'\n', pos)
        print(content[pos:line_end].decode('utf-8'))

if __name__ == "__main__":
    check_columns()
