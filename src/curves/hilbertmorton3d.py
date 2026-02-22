import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from hilbertcurve.hilbertcurve import HilbertCurve
import pymorton

def courbe_hilbert_3d(order):
    n = 3
    hilbert = HilbertCurve(order, n)
    nb_points = 2 ** (order * n)
    return np.array([hilbert.point_from_distance(i) for i in range(nb_points)])

def courbe_zorder_3d(order):
    max_coord = 2 ** order
    coords = []
    nb_points = max_coord ** 3
    for i in range(nb_points):
        try:
            x, y, z = pymorton.deinterleave3(i)
            if x < max_coord and y < max_coord and z < max_coord:
                coords.append([x, y, z])
        except Exception:
            continue
    return np.array(coords)

ordre = 2

hilbert_points = courbe_hilbert_3d(ordre)
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(hilbert_points[:,0], hilbert_points[:,1], hilbert_points[:,2], 'r-', linewidth=1)
ax.axis('off')
plt.tight_layout()
plt.savefig(f"hilbert{ordre}.pdf", bbox_inches='tight', facecolor='white')
plt.close()

zorder_points = courbe_zorder_3d(ordre)
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(zorder_points[:,0], zorder_points[:,1], zorder_points[:,2], 'b-', linewidth=1)
ax.axis('off')
plt.tight_layout()
plt.savefig(f"morton{ordre}.pdf", bbox_inches='tight', facecolor='white')
plt.close()
