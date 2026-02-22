import matplotlib.pyplot as plt
import numpy as np
from hilbertcurve.hilbertcurve import HilbertCurve
def courbe_hilbert(ordre):
    n,p=2,ordre
    courbe = HilbertCurve(p, n)
    nb_points = 2 ** (p * n)
    coordonnees = []
    for i in range(nb_points):
        point = courbe.point_from_distance(i)
        coordonnees.append(point)
    return np.array(coordonnees)
for ordre in [1, 2, 3]:
    points = courbe_hilbert(ordre)
    plt.figure(figsize=(5, 5))
    plt.plot(points[:, 0], points[:, 1], 'r-', linewidth=8)
    plt.axis('off')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(f"hilbert_{ordre}.pdf",facecolor='white'\
        ,bbox_inches="tight")
    plt.close()
