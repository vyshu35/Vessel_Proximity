import pandas as pd
import numpy as np
import os
import plotly.express as px

working_directory = r'D:\SKYSERVE ASSIGNMENT\Vessel_proximity'
input_file = os.path.join(working_directory, 'sample_data.csv')
# Load data
data = pd.read_csv(input_file)

# Plot vessel positions using Plotly
fig = px.scatter_mapbox(data, lat='lat', lon='lon', color='mmsi',
                        hover_name='mmsi', zoom=3, height=600)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(title='Vessel Positions')

# Save the plot to the working directory
save = os.path.join(working_directory, 'vessel_positions_plotly.html')
fig.write_html(save)
