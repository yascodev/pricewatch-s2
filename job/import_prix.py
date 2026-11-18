"""PriceWatch — job d'import (VERSION DE DÉPART, volontairement gourmande).

Lit l'historique brut des relevés et calcule, pour chaque produit, magasin et mois
depuis 2020 : le prix minimum, maximum et moyen TTC, le prix moyen hors taxes
(TVA alimentaire à 5,5 %) et le nombre de relevés. Écrit le résultat dans out/monthly.csv.

Le job affiche ce qu'il a consommé à la fin : ne touchez pas au bloc « Mesures ».
"""
import resource
import time
from pathlib import Path

import pandas as pd

DATA_DIR = Path("/data") if Path("/data").exists() else Path(__file__).resolve().parent.parent / "data"
SRC = DATA_DIR / "raw" / "history.csv"
OUT = DATA_DIR / "out" / "monthly.csv"

start = time.perf_counter()

# 1. On charge tout le fichier
df = pd.read_csv(SRC)

# 2. On garde une copie de travail, « au cas où »
work = df.copy()

# 3. On extrait l'année et le mois de chaque date
work["year"] = work["date"].apply(lambda d: int(d[:4]))
work["month"] = work["date"].apply(lambda d: d[:7])

# 4. On calcule le prix hors taxes, ligne par ligne
work["price_ht"] = work.apply(lambda row: row["price"] / 1.055, axis=1)

# 5. On ne garde que les relevés depuis 2020
work = work[work["year"] >= 2020]

# 6. On agrège
result = (
    work.groupby(["product", "shop", "month"])
    .agg(
        price_min=("price", "min"),
        price_max=("price", "max"),
        price_mean=("price", "mean"),
        price_ht_mean=("price_ht", "mean"),
        count=("price", "count"),
    )
    .round(2)
    .reset_index()
    .sort_values(["product", "shop", "month"])
)

OUT.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUT, index=False)

# --- Mesures (ne pas modifier) -------------------------------------------------
wall = time.perf_counter() - start
usage = resource.getrusage(resource.RUSAGE_SELF)
cpu = usage.ru_utime + usage.ru_stime
print(f"Lignes écrites       : {len(result)}")
print(f"Temps réel           : {wall:6.1f} s")
print(f"Temps CPU (user+sys) : {cpu:6.1f} s  (ratio CPU / réel : {cpu / wall:.2f})")
print(f"Pic de RAM (RSS)     : {usage.ru_maxrss / 1024:6.0f} Mo")
