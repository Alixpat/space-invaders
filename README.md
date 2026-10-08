# Space Invaders (façon Atari 2600)

Un Space Invaders en Python inspiré de la version Atari 2600 de 1980 :
6 rangées d'envahisseurs, 3 boucliers destructibles, une soucoupe mystère,
gros pixels larges et sons synthétisés.

Tout est généré par le code (sprites, police, sons) : le jeu tient dans un seul
fichier, `jeu.py`, et n'a besoin d'aucune image ni d'aucun son externe.

## 1. Paquets système (Ubuntu / Debian)

```bash
sudo apt install python3-venv python3-pip
```

## 2. Dossier du jeu + environnement virtuel

```bash
cd space-invaders
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt     # installe pygame-ce
```

Le dossier `.venv/` est ignoré par git : chacun le recrée sur sa machine.

## 3. Vérifier que pygame fonctionne

```bash
python -m pygame.examples.aliens
```

Une fenêtre de jeu doit s'ouvrir avec du son. Si c'est le cas, tout est prêt.

## 4. Lancer le jeu

```bash
.venv/bin/python jeu.py
```

(ou simplement `python jeu.py` si le venv est activé).

La fenêtre est redimensionnable : étire-la ou agrandis-la, l'image suit en
gardant ses proportions.

## Commandes

| Touche                    | Action                       |
|---------------------------|------------------------------|
| ← / → (ou Q / D, A / D)   | Déplacer le canon            |
| Espace (ou ↑)             | Tirer                        |
| P                         | Pause                        |
| C                         | Effet télé (lignes) on/off   |
| Échap                     | Quitter                      |

## Règles

- Un seul tir à l'écran à la fois, comme sur la console d'origine.
- Points : de 5 (rangée du bas) à 30 (rangée du haut) ; la soucoupe rapporte
  50, 100, 150 ou 300 points.
- Les envahisseurs accélèrent à mesure qu'ils tombent, et chaque nouvelle vague
  commence un peu plus bas.
- Partie perdue quand il ne reste plus de vies ou quand les envahisseurs
  atteignent le sol.
- Le record est enregistré dans `record.txt`.
