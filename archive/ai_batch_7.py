# -*- coding: utf-8 -*-
# AI Update Batch 7 - Remaining cities
import subprocess, sys
cities = [
    "Nowy Sącz", "Zabrze", "Chorzów", "Siedlce", "Dąbrowa Górnicza",
    "Grudziądz", "Kalisz", "Wałbrzych", "Konin", "Tarnów",
    "Włocławek", "Piła", "Słupsk", "Tychy", "Legnica",
    "Ruda Śląska", "Piotrków Trybunalski", "Inowrocław", "Zakopane",
    "Mysłowice", "Jastrzębie-Zdrój", "Jaworzno", "Lubin"
]
cmd = [sys.executable, "update_city_review_ai.py"] + cities + ["--limit", "10", "--skip-existing"]
print("Running:", " ".join(cmd))
subprocess.run(cmd)
