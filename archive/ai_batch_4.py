# -*- coding: utf-8 -*-
# AI Update Batch 4
import subprocess, sys
cities = ["Częstochowa", "Gdynia", "Rzeszów", "Olsztyn", "Opole"]
cmd = [sys.executable, "update_city_review_ai.py"] + cities + ["--limit", "10", "--skip-existing"]
print("Running:", " ".join(cmd))
subprocess.run(cmd)
