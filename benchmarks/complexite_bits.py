import time
import numpy as np
from hilbertcurve.hilbertcurve import HilbertCurve
import pymorton
import matplotlib.pyplot as plt

# Configuration
dimensions = 3
bits = 2  # we will vary this to see impact on hilbert time

def benchmark_hilbertcurve(n_trials, bits):
    dimensions = 3
    hilbert = HilbertCurve(p=bits, n=dimensions)
    max_coord = 2 ** bits
    points = np.random.randint(0, max_coord, size=(n_trials, dimensions))

    start = time.perf_counter()
    for i, pt in enumerate(points):
        pt_tuple = tuple(int(x) for x in pt)
        if len(pt_tuple) != dimensions:
            print(f"⛔ ERREUR À l’itération {i}: {pt_tuple} (taille {len(pt_tuple)})")
            continue  # ignorer ce point pour ne pas planter
        hilbert.distance_from_point(pt_tuple)
    end = time.perf_counter()
    return (end - start) / n_trials


def benchmark_morton(n_trials, bits):
    max_coord = 2 ** bits
    points = np.random.randint(0, max_coord, size=(n_trials, 3))

    start = time.perf_counter()
    for pt in points:
        pymorton.interleave3(int(pt[0]), int(pt[1]), int(pt[2]))
    end = time.perf_counter()
    return (end - start) / n_trials  # time per call

# Tests sur différentes tailles (bits = précision par dimension)
bit_range = range(1, 11)
n_trials = 10000
hilbert_times = []
morton_times = []

for b in bit_range:
    print(f"Testing for bits = {b}")
    hilbert_time = benchmark_hilbertcurve(n_trials, b)
    morton_time = benchmark_morton(n_trials, b)
    hilbert_times.append(hilbert_time)
    morton_times.append(morton_time)

# Plot
plt.figure(figsize=(8,5))
plt.plot(bit_range, hilbert_times, label="HilbertCurve.distance_from_point", marker='o')
plt.plot(bit_range, morton_times, label="pymorton.interleave3", marker='s')
plt.xlabel("Bits (précision par dimension)")
plt.ylabel("Temps moyen par appel (secondes)")
plt.title("Benchmark Hilbert vs Morton")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("benchmark_CRE.pdf")
plt.show()
