
import subprocess, sys
# Batch 4: Gorzów Wielkopolski - Jaworzno
cities = ["Gorzów Wielkopolski", "Inowrocław", "Jastrzębie-Zdrój", "Jaworzno"]
def run_batch():
    for city in cities:
        print(f"\n--- STARTING: {city} ---")
        try:
            subprocess.run([sys.executable, "run_updates.py", "--city", city, "--limit", "10"], check=True)
            print(f"✓ FINISHED: {city}")
        except Exception as e: print(f"❌ ERROR: {e}")
if __name__ == "__main__": run_batch()
