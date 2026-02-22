import time
import numpy as np
import matplotlib.pyplot as plt
from hilbertcurve.hilbertcurve import HilbertCurve
import pymorton

# Définir les composants de couleur (4 valeurs → 64 combinaisons)
components = [0, 85, 170, 255]

def generate_colors():
    return [(r, g, b) for r in components for g in components for b in components]

# Sweep: tri lexicographique
def sweep_order(colors):
    return sorted(colors, key=lambda c: (c[0], c[1], c[2]))

# Scan: boustrophédon ligne/colonne
def scan_order(colors):
    sorted_colors = sorted(colors, key=lambda c: (c[0], c[1], c[2]))
    scan_ordered = []
    for i in range(0, len(sorted_colors), 8):
        row = sorted_colors[i:i+8]
        if (i // 8) % 2 == 0:
            scan_ordered.extend(row)
        else:
            scan_ordered.extend(row[::-1])
    return scan_ordered

# Hilbert
def hilbert_order(colors):
    hilbert = HilbertCurve(p=2, n=3)
    color_to_index = {}
    for color in colors:
        scaled = tuple(c // 85 for c in color)
        color_to_index[color] = hilbert.distance_from_point(scaled)
    return sorted(colors, key=lambda c: color_to_index[c])

# Morton
def morton_order(colors):
    def morton_key(c):
        r, g, b = (c[0] // 85, c[1] // 85, c[2] // 85)
        return pymorton.interleave3(int(r), int(g), int(b))
    return sorted(colors, key=morton_key)

# Benchmark d'une méthode
def benchmark(method_fn, colors):
    start = time.perf_counter()
    method_fn(colors)
    end = time.perf_counter()
    return end - start

# Préparer la mesure
methods = {
    "Sweep": sweep_order,
    "Scan": scan_order,
    "Hilbert": hilbert_order,
    "Morton": morton_order
}

# Effectuer les mesures
colors = generate_colors()
results = {}

for name, method in methods.items():
    duration = benchmark(method, colors)
    results[name] = duration
    print(f"{name} trié en {duration:.6f} secondes.")

# Affichage graphique
plt.figure(figsize=(8,5))
plt.bar(results.keys(), results.values(), color=['steelblue', 'orchid', 'orange', 'green'])
plt.ylabel("Temps de tri (secondes)")
plt.title("Temps de tri pour 64 couleurs RGB (4 valeurs / canal)")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig("../data/output/benchmark_sorting_comparison.png", dpi=150, bbox_inches='tight')
plt.savefig("benchmark_sorting_comparison.pdf")  # Keep PDF for archival
plt.show()
