import matplotlib.pyplot as plt
import numpy as np

# Define the number of UAVs and the distance between them
num_rows = 5
num_cols = 3
distance = 50

# Generate positions for UAVs in a cone formation
positions = []
for row in range(num_rows):
    for col in range(num_cols):
        x = col * distance + (row % 2) * (distance / 2)
        y = row * distance
        positions.append((x, y))

# Convert positions to numpy arrays for easier plotting
positions = np.array(positions)

# Plot the UAV positions
plt.figure(figsize=(8, 6))
plt.scatter(positions[:, 0], positions[:, 1], c='black')

# Annotate the UAVs with their labels
for i, (x, y) in enumerate(positions):
    plt.text(x, y, f'FY{i+1:02d}', fontsize=12, ha='right')

# Set plot title and labels
plt.title('Cone Formation of UAVs')
plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')

plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')

# Save the plot to a file
# plt.savefig('/mnt/data/cone_formation.png')
plt.show()
