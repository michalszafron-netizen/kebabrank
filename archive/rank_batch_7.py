
import subprocess, sys
# Batch 7: Lublin - Olsztyn
cities = ["Lublin", "Myslowice", "Myszków", "Nowy Sącz", "Olsztyn"]
def run_batch():
    for city in cities:
        print(f"\n--- STARTING: {city} ---")
        try:
            subprocess.run([sys.executable, "run_updates.py", "--city", city, "--limit", "10"], check=True)
            print(f"✓ FINISHED: {city}")
        except Exception as e: print(f"❌ ERROR: {e}")
if __name__ == "__main__": run_batch()
