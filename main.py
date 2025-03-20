import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.animation as animation

# Read the dataset
def read_dataset(filename):
    with open(filename, "r") as file:
        return np.array([[int(bit) for bit in line.strip()] for line in file])

matrix = read_dataset("dataset.txt")
rows, cols = matrix.shape

# Find 1s, ordered from top-left to bottom-right
ones = {(i, j) for i in range(rows) for j in range(cols) if matrix[i][j] == 1}

# Create figure and plot grid
fig, ax = plt.subplots(figsize=(cols, rows))
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(-0.5, cols - 0.5)
ax.set_ylim(rows - 0.5, -0.5)
ax.set_frame_on(False)

# Draw grid
patches = {}
for i in range(rows):
    for j in range(cols):
        color = "green" if (i, j) in ones else "cyan"
        rect = Rectangle((j - 0.5, i - 0.5), 1, 1, color=color, ec='white')
        ax.add_patch(rect)
        patches[(i, j)] = rect

def calculate_perimeter(ones):
    total_perimeter = 0
    edge_data = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    edges_info = {(-1, 0): ((0, -0.5), 1, 0.05), (1, 0): ((0, 0.45), 1, 0.05),
                  (0, -1): ((-0.5, 0), 0.05, 1), (0, 1): ((0.45, 0), 0.05, 1)}

    for i, j in ones:
        edges = [(j + dx, i + dy, edges_info[(dx, dy)]) 
                 for dx, dy in directions if (i + dx, j + dy) not in ones]  # #
        perimeter += len(edges)
        edge_data.append(((i, j), edges))

    return edge_data, perimeter
    
    edge_data, total_perimeter = calculate_perimeter(ones)

def update(frame):
    if frame < len(edge_data):
        (i, j), edges = edge_data[frame]
        patches[(i, j)].set_color('red')
        
        for x, y, (offset, w, h) in edges:
            ax.add_patch(Rectangle((x + offset[0], y + offset[1]), w, h, color='yellow'))
        
        # Restore previous rectangle's color after animation proceeds
        if frame > 0:
            prev_i, prev_j = edge_data[frame - 1][0]
            patches[(prev_i, prev_j)].set_color('green')
        
        # Restore last red square back to cyan at the end
        if frame == len(edge_data) - 1:
            patches[(i, j)].set_color('green')
            ax.text(0.35, -0.75, f"Perimeter: {total_perimeter}", fontsize=12, ha="center", color="black", weight="bold")

    return ax.patches

ani = animation.FuncAnimation(fig, update, frames=len(edge_data), interval=100, repeat=False)
plt.show()
