import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.animation as animation

# Read the dataset
with open("dataset.txt", "r") as file:
    matrix = [list(line.strip()) for line in file]

# Convert to integers
matrix = np.array([[int(bit) for bit in row] for row in matrix])
rows, cols = matrix.shape

# Find 1s, ordered from top-left to bottom-right
ones = [(i, j) for i in range(rows) for j in range(cols) if matrix[i][j] == 1]

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
        color = "green" if matrix[i][j] == 1 else "cyan"
        rect = Rectangle((j - 0.5, i - 0.5), 1, 1, color=color, ec='white')
        ax.add_patch(rect)
        patches[(i, j)] = rect

edge_data = []
total_perimeter = 0

for i, j in ones:
    edges = []
    if (i - 1, j) not in ones:
        edges.append(((j - 0.5, i - 0.5), 1, 0.05))
        total_perimeter += 1
    if (i + 1, j) not in ones:
        edges.append(((j - 0.5, i + 0.45), 1, 0.05))
        total_perimeter += 1
    if (i, j - 1) not in ones:
        edges.append(((j - 0.5, i - 0.5), 0.05, 1))
        total_perimeter += 1
    if (i, j + 1) not in ones:
        edges.append(((j + 0.45, i - 0.5), 0.05, 1))
        total_perimeter += 1
    
    edge_data.append((i, j, edges))

def update(frame):
    if frame < len(edge_data):
        i, j, edges = edge_data[frame]
        
        # Set the current rectangle's color to red
        patches[(i, j)].set_color('red')
        
        for pos, w, h in edges:
            ax.add_patch(Rectangle(pos, w, h, color='yellow'))
        
        # Restore previous rectangle's color after animation proceeds
        if frame > 0:
            prev_i, prev_j, _ = edge_data[frame - 1]
            patches[(prev_i, prev_j)].set_color('green')
        
        # Restore last red square back to cyan at the end
        if frame == len(edge_data) - 1:
            patches[(i, j)].set_color('green')
            
            # Add the text message at the final frame
            ax.text(0.35, -0.75, f"Perimeter: {total_perimeter}", 
                    fontsize=12, ha="center", color="black", weight="bold")

    return ax.patches

ani = animation.FuncAnimation(fig, update, frames=len(edge_data), interval=100, repeat=False)
plt.show()
