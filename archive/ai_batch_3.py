# -*- coding: utf-8 -*-
# AI Update Batch 3
import subprocess, sys
cities = ["Lublin", "Białystok", "Bydgoszcz", "Katowice"]
cmd = [sys.executable, "update_city_review_ai.py"] + cities + ["--limit", "10", "--skip-existing"]
print("Running:", " ".join(cmd))
subprocess.run(cmd)
