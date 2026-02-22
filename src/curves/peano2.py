import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from functools import lru_cache

@lru_cache(maxsize=None)
def get_peano_coords(level: int) -> np.ndarray:
    """
    Recursively generates the coordinates for the Peano curve of a given level.
    Uses memoization to cache results for efficiency.
    """
    if level == 1:
        # Base case: The 9 points for the 3x3 grid in the first iteration.
        return np.array([
            (0, 0), (0, 1), (0, 2),
            (1, 2), (1, 1), (1, 0),
            (2, 0), (2, 1), (2, 2)
        ])

    # Recursive step: Generate the curve from the previous level.
    prev_coords = get_peano_coords(level - 1)
    side = 3**(level - 1)
    
    # The main path follows the pattern of the first-level curve.
    main_path_template = get_peano_coords(1)
    
    all_coords = []
    for i, (mx, my) in enumerate(main_path_template):
        # Create a copy of the previous level's coordinates for transformation.
        sub_coords = np.copy(prev_coords)

        # Transformation Rule 1: Flip vertically for the middle column.
        if i in {3, 4, 5}:
            sub_coords[:, 1] = (side - 1) - sub_coords[:, 1]
            
        # Transformation Rule 2: Reverse path for every second segment to connect ends.
        if i % 2 == 1:
            sub_coords = sub_coords[::-1]

        # Translate the transformed sub-curve to its correct position in the main grid.
        offset = np.array([mx * side, my * side])
        all_coords.append(sub_coords + offset)
        
    return np.vstack(all_coords)

def draw_peano(ax: plt.Axes, level: int):
    """
    Draws the Peano curve and its grid for a specific level on a given matplotlib axis.
    """
    coords = get_peano_coords(level)
    # Scale coordinates to be in the center of the grid cells.
    scaled_coords = coords + 0.5
    
    grid_size = 3**level
    
    # Set plot appearance
    ax.set_aspect('equal')
    ax.set_facecolor('#f7f7f7')
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor('black')

    # Plot the curve
    ax.plot(
        scaled_coords[:, 0], scaled_coords[:, 1],
        color='#990000',  # Dark red
        linewidth=2.0
    )

    # Draw the sub-grid (thin lines)
    ax.grid(True, which='major', color='gray', linestyle='-', linewidth=0.5)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))

    # Draw the main 3x3 grid (thick lines) if level > 1
    if level > 1:
        major_grid_size = 3**(level - 1)
        ax.xaxis.set_major_locator(MultipleLocator(major_grid_size))
        ax.yaxis.set_major_locator(MultipleLocator(major_grid_size))
        ax.grid(True, which='major', color='black', linestyle='-', linewidth=1.5)

    # Add the direction arrow at the end of the curve
    start_arrow = scaled_coords[-2]
    end_arrow = scaled_coords[-1]
    dx = end_arrow[0] - start_arrow[0]
    dy = end_arrow[1] - start_arrow[1]
    
    # Scale arrow size based on the grid size
    head_width = 0.05 * (3**level)
    ax.arrow(
        start_arrow[0], start_arrow[1], dx, dy,
        head_width=head_width,
        head_length=head_width * 1.5,
        fc='black',
        ec='black',
        length_includes_head=True
    )

def main():
    """
    Main function to create and display the plot with the three iterations.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6.5))
    fig.suptitle('Peano Curve Iterations in Python', fontsize=20)
    
    levels = [1, 2, 3]
    titles = ["Level 1 (3x3 Grid)", "Level 2 (9x9 Grid)", "Level 3 (27x27 Grid)"]

    for i, level in enumerate(levels):
        ax = axes[i]
        draw_peano(ax, level)
        ax.set_title(titles[i], fontsize=14)
        
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

if __name__ == '__main__':
    main()
