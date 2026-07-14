# -*- coding: utf-8 -*-
# AI Update Batch 5
import subprocess, sys
cities = ["Radom", "Toruń", "Zielona Góra", "Kielce", "Rybnik", "Elbląg"]
cmd = [sys.executable, "update_city_review_ai.py"] + cities + ["--limit", "10", "--skip-existing"]
print("Running:", " ".join(cmd))
subprocess.run(cmd)
