# SOBRIETE.md · PriceWatch

Groupe :
Machine de mesure (OS, processeur, RAM allouée à Docker) :

## Séance 2 · Le job sous contrainte

Cible : 256 Mo de RAM, 1 CPU, moins de 30 s, résultat identique.

| Étape | Limites (RAM · CPU) | Pic de RAM (Mo) | Temps réel (s) | Temps CPU (s) | Ratio CPU / réel | Code de sortie | OOMKilled |
|---|---|---|---|---|---|---|---|
| 01. Ligne de base | aucune | | | | | | |
| 02a. Sous contrainte | 256m · 1 | | | | | | |
| 02b. CPU réduit | aucune · 0.5 | | | | | | |
| 03. Optimisation RAM | 256m · 1 | | | | | | |
| 04. Optimisation CPU | 256m · 1 | | | | | | |
| 05. Dimensionné | ? · ? | | | | | | |
| Bonus | | | | | | | |

### Ce que nous avons changé, et pourquoi (une ligne par changement)

-

### Dimensionnement retenu

Commande de lancement finale :

    docker run ...

Justification (pic mesuré, marge choisie) :

### Ce que nous en retenons (3 lignes maximum)

-
