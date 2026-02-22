#  Space-Filling Curves & Image Processing

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Mathématiques](https://img.shields.io/badge/Math%C3%A9matiques-Mod%C3%A9lisation-orange)
![TIPE](https://img.shields.io/badge/TIPE-2025-success)

##  À propos du projet
Ce dépôt contient le code source de mon projet TIPE. Il explore les propriétés mathématiques des **courbes remplissant l'espace** (Hilbert, Morton/Z-Order, Peano) et propose une implémentation logicielle de leurs applications en **traitement d'images**, en **tramage (dithering)** et en **optimisation de la compression sans perte**.

L'objectif de ce projet est de démontrer comment la modification du parcours spatial d'une image matricielle classique (de linéaire vers fractal) permet d'optimiser l'efficacité des algorithmes standards de compression et de traitement.

##  Architecture Fonctionnelle

Le code est structuré de manière modulaire autour de plusieurs axes :

### 1. Modélisation Mathématique (`src/curves.py`)
- Génération récursive et calcul d'index pour les courbes de **Hilbert** (`hilbertcurve`), **Morton** (`pymorton`) et **Peano**.
- Adaptation de ces parcours bijectifs $[0,1] \to [0,1]^2$ aux grilles discrètes (images matricielles).

### 2. Traitement d'Images (`src/dithering.py`)
Implémentation complète d'algorithmes de diffusion d'erreurs :
- **Algorithme d'Atkinson** (adapté pour suivre les parcours fractals générés).
- **Algorithme de Floyd-Steinberg**.
- Passage en niveaux de gris et quantification N-bits (`src/utils_image.py`).

### 3. Métriques et Compression (`src/compression.py`)
- Calcul de l'**entropie de Shannon** avec `scipy.stats` sur les images traitées.
- Simulation d'un pipeline de compression sans perte en comparant le poids brut (`.raw`) avec l'encodage `gzip`.

### 4. Tri Lexicographique des Couleurs (`src/color_sorting.py`)
- Expérimentations sur le tri de palettes RGB (64 couleurs) via différentes heuristiques : *Sweep* (lexicographique), *Scan* (boustrophédon), et parcours fractals (Hilbert, Morton).

##  Résultats Principaux

L'approche de dithering (Atkinson) guidée par la courbe de Hilbert préserve la localité bidimensionnelle bien mieux qu'un parcours linéaire ("Serpent"). 

**Sur une image de test classique :**
- Réduction spectaculaire du poids du fichier post-compression GZIP.
- **Réduction totale mesurée : jusqu'à -88.9 %** du poids de l'image (de ~38 Ko à ~4 Ko).
- L'étude de complexité (`benchmarks/`) montre que le parcours de Morton est environ 10× plus rapide à calculer que Hilbert, au prix d'une perte d'efficience sur la compression (sauts spatiaux plus importants).

##  Installation

Clonez ce dépôt et installez les dépendances requises :

```bash
git clone https://github.com/ton-pseudo/TIPE-SpaceFillingCurves.git
cd TIPE-SpaceFillingCurves
pip install -r requirements.txt
