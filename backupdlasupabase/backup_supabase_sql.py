import os
import subprocess
import datetime
from urllib.parse import quote_plus

# Session pooler connection string (IPv4 compatible)
# Connection string: postgresql://postgres.shimhhadhsntguwubeiv:Jebacsql@23@aws-0-eu-north-1.pooler.supabase.com:5432/postgres
password = "Jebacsql@23"
encoded_password = quote_plus(password)
conn_string = f"postgresql://postgres.shimhhadhsntguwubeiv:{encoded_password}@aws-0-eu-north-1.pooler.supabase.com:5432/postgres"

# Create backups directory
backup_dir = "backups"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Timestamped filename
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = os.path.join(backup_dir, f"supabase_dump_{timestamp}.sql")
output_file_abs = os.path.abspath(output_file)

print(f"Starting SQL structure and data backup to {output_file}...")
print("Using pooling connection (IPv4) and Docker postgres:17...")

# Check if pg_dump is available natively
try:
    subprocess.run(["pg_dump", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    use_docker = False
    print("pg_dump found locally.")
except (FileNotFoundError, subprocess.CalledProcessError):
    print("pg_dump not found locally. Using Docker...")
    use_docker = True

if use_docker:
    # Use postgres:17 to match your Supabase version
    cmd = [
        "docker", "run", "--rm", "postgres:17",
        "pg_dump", "--clean", "--if-exists", "--quote-all-identifiers", conn_string
    ]
else:
    cmd = [
        "pg_dump", "--clean", "--if-exists", "--quote-all-identifiers", conn_string
    ]

try:
    with open(output_file_abs, "w", encoding="utf-8") as f:
        print("Executing pg_dump... this may take a moment.")
        process = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        
        if process.returncode != 0:
            print(f"Error executing backup:\n{process.stderr}")
        else:
            print(f"Backup completed successfully! Saved to: {output_file_abs}")
            
except Exception as e:
    print(f"An unexpected error occurred: {e}")
