# Awalé

Jeu d’Awalé en Python avec interface graphique Tkinter.

## Prérequis

- Python 3.11 ou plus
- `tkinter` installé sur le système
- `pip`

Sur Arch Linux :

```bash
sudo pacman -S python tk
```

## Installation

```bash
git clone https://github.com/AxelGiovannai/Awale
cd Awale
```

Créer un environnement virtuel :
```bash
python -m venv .venv
```

Activer le venv :

```bash
source .venv/bin/activate
```

Lancer le projet :
```bash
python Main.py
```

## Structure du projet

- Main.py : point d’entrée
- Awale.py : logique du jeu
- GameController.py : gestion de la partie
- Gui_tkinter.py : interface graphique
- Human.py : interaction joueur
- Statistic.py : statistiques du projet
