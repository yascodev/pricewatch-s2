# PriceWatch · Kit de la séance 2 : le job sous contrainte

Le job `job/import_prix.py` lit l'historique brut des relevés de prix (3 millions de lignes,
environ 230 Mo) et calcule les statistiques mensuelles par produit et par magasin depuis 2020.
Il écrit le résultat dans `data/out/monthly.csv`.

Il fonctionne, mais il consomme beaucoup. Votre mission : le faire tenir dans
**256 Mo de RAM et 1 CPU, en moins de 30 secondes**, sans changer son résultat.

## 1. Démarrer

    docker build -t pw-job .

    # Générer les données (une seule fois, ~10 s, ~230 Mo)
    docker run --rm -v "$PWD/data:/data" pw-job python job/generate_history.py

    # Lancer le job, sans limite
    docker run --rm -v "$PWD/data:/data" pw-job

Sous Windows PowerShell, écrivez `${PWD}` au lieu de `$PWD`.

À la fin, le job affiche trois mesures : temps réel, temps CPU (et le ratio CPU / réel), pic de RAM.
Notez-les dans `SOBRIETE.md`.

## 2. Lancer sous contrainte

    docker run --name pw --memory=256m --memory-swap=256m --cpus=1 \
      -v "$PWD/data:/data" pw-job

    docker inspect --format 'Code de sortie : {{.State.ExitCode}} · OOMKilled : {{.State.OOMKilled}}' pw
    docker rm pw

`--memory-swap` égal à `--memory` interdit le swap : le conteneur ne peut pas « tricher » sur le disque.

## 3. Observer en direct

Dans un second terminal, pendant que le job tourne :

    docker stats

Colonnes utiles : `CPU %` (100 % = un cœur entier) et `MEM USAGE / LIMIT`.

## 4. Les règles

Vous pouvez modifier :
- `job/import_prix.py`, **sauf le bloc « Mesures »** en fin de fichier ;
- `requirements.txt` et `Dockerfile`, si vous le justifiez dans `SOBRIETE.md`.

Le fichier `data/out/monthly.csv` doit rester identique à celui produit par la version de départ :
mêmes lignes, mêmes colonnes, même ordre. Un écart d'un centime sur quelques moyennes est toléré
(les additions de nombres à virgule ne donnent pas exactement le même résultat selon leur ordre).

Conseil : avant de toucher au code, copiez le résultat de référence.

    cp data/out/monthly.csv data/out/reference.csv

## 5. En cas de problème

- **`Permission denied` sur `/data/out` (Linux)** : le conteneur tourne avec l'utilisateur 1000.
  `sudo chown -R 1000:1000 data/` ou lancez avec `--user "$(id -u):$(id -g)"`.
- **Le job s'arrête sans message d'erreur** : regardez le code de sortie et `OOMKilled` (section 2).
- **Docker Desktop (Mac / Windows)** : vérifiez la RAM allouée à la VM Docker
  (Settings › Resources). Il faut au moins 4 Go pour la ligne de base.
