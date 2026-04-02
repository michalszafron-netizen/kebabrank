# -*- coding: utf-8 -*-
# AI Update Batch 2
import subprocess, sys
cities = ["Gdańsk", "Łódź", "Poznań", "Szczecin"]
cmd = [sys.executable, "update_city_review_ai.py"] + cities + ["--limit", "10", "--skip-existing"]
print("Running:", " ".join(cmd))
subprocess.run(cmd)
