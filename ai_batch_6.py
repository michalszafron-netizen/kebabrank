# -*- coding: utf-8 -*-
# AI Update Batch 6
import subprocess, sys
cities = ["Sosnowiec", "Gorzów Wielkopolski", "Gliwice", "Bielsko-Biała", "Koszalin", "Płock", "Bytom"]
cmd = [sys.executable, "update_city_review_ai.py"] + cities + ["--limit", "10", "--skip-existing"]
print("Running:", " ".join(cmd))
subprocess.run(cmd)
