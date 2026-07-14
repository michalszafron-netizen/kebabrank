
import subprocess, sys
# Batch 2: Bytom - Dobczyce
cities = ["Bytom", "Chorzów", "Czechowice-Dziedzice", "Częstochowa", "Dobczyce"]
def run_batch():
    for city in cities:
        print(f"\n--- STARTING: {city} ---")
        try:
            subprocess.run([sys.executable, "run_updates.py", "--city", city, "--limit", "10"], check=True)
            print(f"✓ FINISHED: {city}")
        except Exception as e: print(f"❌ ERROR: {e}")
if __name__ == "__main__": run_batch()
