"""Génère l'historique brut des relevés de prix PriceWatch.

Usage :
    python generate_history.py            # 3 000 000 lignes, environ 230 Mo
    python generate_history.py 500000     # moins de lignes pour tester vite
"""
import csv
import random
import sys
from pathlib import Path

DATA_DIR = Path("/data") if Path("/data").exists() else Path(__file__).resolve().parent.parent / "data"
OUT = DATA_DIR / "raw" / "history.csv"
ROWS = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000

PRODUCTS = {
    "cafe-moulu-250g": 3.20, "lait-demi-ecreme-1l": 1.05, "baguette": 1.15,
    "huile-olive-1l": 9.80, "riz-basmati-1kg": 2.90, "pommes-1kg": 2.40,
    "beurre-doux-250g": 2.60, "oeufs-x12": 3.90, "pates-500g": 1.30, "yaourt-nature-x4": 1.70,
}
SHOPS = ["Paris-11", "Paris-15", "Levallois", "Lyon-3", "Lyon-7", "Lille-Centre",
         "Marseille-6", "Nantes-Est", "Bordeaux-Centre", "Toulouse-Capitole"]

OUT.parent.mkdir(parents=True, exist_ok=True)
random.seed(42)
names = list(PRODUCTS)

with OUT.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "shop", "product", "price", "source_id", "comment"])
    for i in range(ROWS):
        p = random.choice(names)
        year = random.randint(2015, 2026)
        date = f"{year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        # inflation simple : +2,5 % par an depuis 2015, plus du bruit
        price = PRODUCTS[p] * (1.025 ** (year - 2015)) * random.uniform(0.9, 1.1)
        w.writerow([date, random.choice(SHOPS), p, f"{price:.2f}", f"src-{i:08d}",
                    "releve-automatique" if i % 7 else "releve-manuel-verifie-par-operateur"])

print(f"{OUT} : {ROWS:,} lignes, {OUT.stat().st_size / 1e6:.0f} Mo".replace(",", " "))
