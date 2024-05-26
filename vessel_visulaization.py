import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

working_directory = r'D:\SKYSERVE ASSIGNMENT\Vessel_proximity'
input_file = os.path.join(working_directory, 'sample_data.csv')
# Load data
data = pd.read_csv(input_file)

# Plot vessel positions with color variation based on mmsi
fig, ax = plt.subplots(figsize=(10, 6))

unique_mmsi = data['mmsi'].unique()
colors = plt.cm.jet(np.linspace(0, 1, len(unique_mmsi)))
color_map = dict(zip(unique_mmsi, colors))

# Apply color mapping to mmsi and create the 'color' column
data['color'] = data['mmsi'].map(color_map)

# Create the scatter plot
scatter = ax.scatter(data['lon'], data['lat'], s=10, c=data['color'], alpha=0.5)

# Create a colorbar
norm = mcolors.Normalize(vmin=0, vmax=len(unique_mmsi))
sm = plt.cm.ScalarMappable(cmap=plt.cm.jet, norm=norm)
sm.set_array([])  # Only needed for matplotlib < 3.1

# Specify the Axes for the Colorbar and adjust its position
cbar_ax = fig.add_axes([0.85, 0.1, 0.02, 0.8])  # Adjust left parameter here
cbar = fig.colorbar(sm, cax=cbar_ax, ticks=np.linspace(0, len(unique_mmsi), len(unique_mmsi)))
cbar.set_ticklabels(unique_mmsi)
cbar.set_label('MMSI')

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Vessel Positions with MMSI Values')
ax.grid(True)

# Center the plot within the figure
ax.set_aspect('equal')
ax.set_position([0.1, 0.1, 0.7, 0.8])  # [left, bottom, width, height]

# Save the plot
saveplot = os.path.join(working_directory, 'Mapping of vessel positions.png')
plt.savefig(saveplot, bbox_inches='tight')
plt.show()
