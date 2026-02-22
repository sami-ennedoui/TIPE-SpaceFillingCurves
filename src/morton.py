import matplotlib.pyplot as plt
import numpy as np
import pymorton
def generer_points_courbe_z_ordre(ordre_bits):
# ordre = ordre_bits = itération de la courbe , type = int
    max_coordonnee = 2**ordre_bits
    tous_les_points = []
    for y in range(max_coordonnee):
        for x in range(max_coordonnee):
            tous_les_points.append((x, y))
    points_tries_par_z = []
    for x, y in tous_les_points:
        valeur_z = pymorton.interleave2(x, y) 
        points_tries_par_z.append((valeur_z, (x, y)))
    points_tries_par_z.sort()
    coordonnees = np.array([point[1] for point in points_tries_par_z])
    return coordonnees
ordre_courbe = 3
points_courbe = generer_points_courbe_z_ordre(ordre_courbe)
valeur_max = 2**ordre_courbe - 1
points_transformes = np.copy(points_courbe)
points_transformes[:, 0] = valeur_max - points_courbe[:, 1]
points_transformes[:, 1] = valeur_max - points_courbe[:, 0]
# mirroir par rapport à Y
points_courbe = points_transformes 
plt.figure(figsize=(5, 5))
plt.plot(points_courbe[:, 0], points_courbe[:, 1], \
'r-', linewidth=0.75, marker='o', markersize=2, alpha=0.8)
plt.axis('off')
plt.axis('equal')
plt.tight_layout()
plt.savefig(f"Lebesgue{ordre_courbe}.pdf", \
    facecolor='white', bbox_inches="tight")
plt.close()
