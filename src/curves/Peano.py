import matplotlib.pyplot as plt
import numpy as np
from LSpaceCurves import peano_curve

def generer_courbe_peano(ordre):
    """
    Génère les points d'une courbe de Peano d'un ordre donné.

    Args:
        ordre (int): L'ordre de la courbe de Peano. Plus l'ordre est élevé, plus la courbe est détaillée.

    Returns:
        tuple: Un tuple contenant deux listes, les coordonnées x et y de la courbe.
    """
    # Utilise le module 'fractal' pour générer la courbe de Peano
    # La fonction 'peano_curve' retourne une liste de points (x, y)
    points_peano = peano_curve(p)

    # Sépare les coordonnées x et y
    coordonnees_x = [p[0] for p in points_peano]
    coordonnees_y = [p[1] for p in points_peano]

    return coordonnees_x, coordonnees_y

# Définition de l'ordre de la courbe de Peano
ordre_peano = 3

# Génération des points de la courbe de Peano
x_points, y_points = generer_courbe_peano(ordre_peano)

# Création de la figure et du tracé
plt.figure(figsize=(8, 8)) # Définit la taille de la figure pour un aspect carré
plt.plot(x_points, y_points, 'b-', linewidth=1, marker='o', markersize=2, alpha=0.8) # Tracé en bleu

# Désactive les axes pour une meilleure visualisation de la courbe
plt.axis('off')
# Assure que les échelles des axes sont égales pour éviter la distorsion
plt.axis('equal')
# Ajuste la mise en page pour que tout le contenu soit visible
plt.tight_layout()

# Sauvegarde le graphique au format PDF
plt.savefig(f"Peano{ordre_peano}.pdf", facecolor='white', bbox_inches="tight")

# Ferme la figure pour libérer la mémoire
plt.close()
