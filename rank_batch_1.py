
import subprocess
import sys

# Batch 1: Łódź - Bydgoszcz
cities = ["Łódź", "Żarki", "Białystok", "Bielsko-Biała", "Bydgoszcz"]

def run_batch():
    for city in cities:
        print(f"\n{'='*50}")
        print(f">>> STARTING FULL UPDATE FOR: {city} <<<")
        print(f"{'='*50}")
        try:
            # Używamy --limit 10 zgodnie z Twoją prośbą
            subprocess.run([sys.executable, "run_updates.py", "--city", city, "--limit", "10"], check=True)
            print(f"\n✓ FINISHED: {city}")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ ERROR updating {city}: {e}")
        except Exception as e:
            print(f"\n❌ UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    run_batch()
