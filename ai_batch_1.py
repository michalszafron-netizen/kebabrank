# -*- coding: utf-8 -*-
# AI Update Batch 1 - Największe miasta
# Run: python ai_batch_1.py

import subprocess, sys
cities = ["Warszawa", "Kraków", "Wrocław"]
cmd = [sys.executable, "update_city_review_ai.py"] + cities + ["--limit", "10", "--skip-existing"]
print("Running:", " ".join(cmd))
subprocess.run(cmd)
