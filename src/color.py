import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from hilbertcurve.hilbertcurve import HilbertCurve
import pymorton

components = [0, 50, 155, 255]

colors = [(r, g, b) for r in components 
                    for g in components 
                    for b in components]

# 1. Sweep ordering (simple sequential)
def sweep_order(colors):
    #odre lexicographique#
    return sorted(colors, key=lambda c: (c[0], c[1], c[2]))

def scan_order(colors): 
    sorted_colors = sorted(colors, key=lambda c: (c[0], c[1], c[2]))
    
    scan_ordered = []
    for i in range(0, len(sorted_colors), 8):
        if (i//8) % 2 == 0:
            # Forward for even rows
            scan_ordered.extend(sorted_colors[i:i+8])
        else:
            # Backward for odd rows
            scan_ordered.extend(sorted_colors[i+7:i-1:-1])
    return scan_ordered

def hilbert_order(colors):
    hilbert = HilbertCurve(3, 2) 
    color_to_index = {}
    for color in colors:
        scaled = tuple(c//85 for c in color)
        index = hilbert.distance_from_point(scaled)
        color_to_index[color] = index
    return sorted(colors, key=lambda c: color_to_index[c])

def morton_order(colors):
    """Orders colors using Morton/Z-order curve via bit interleaving"""
    def morton_key(color):
        # Scale to 0-3 and interleave bits
        r, g, b = (c//85 for c in color)
        return pymorton.interleave3(r, g, b)
    return sorted(colors, key=morton_key)

# Generate ordered color sequences
methods = {
    "Sweep": sweep_order(colors),
    "Scan": scan_order(colors),
    "Hilbert": hilbert_order(colors),
    "Morton": morton_order(colors)
}

# Create PDF visualizations
for method_name, ordered_colors in methods.items():
    with PdfPages(f'{method_name}color.pdf') as pdf:
        fig, ax = plt.subplots(figsize=(12, 2))
        
        for i, color in enumerate(ordered_colors):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=np.array(color)/255))
            if i % 8 == 0: 
                ax.axvline(i, color='white', linestyle=':', alpha=0.5)
        
        ax.set_xlim(0, len(ordered_colors))
        ax.set_ylim(0, 1)
        ax.axis('off')
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
