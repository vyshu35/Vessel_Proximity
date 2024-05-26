import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
import os


# Haversine formula to calculate distance between two points on the Earth
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    l1, l2 = np.radians(lat1), np.radians(lat2)
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2.0)**2 + np.cos(l1) * np.cos(l2) * np.sin(dlon / 2.0)**2
    c = 2*np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    d = R*c
    return d
# Define input and output directories
working_directory = r'D:\SKYSERVE ASSIGNMENT\Vessel_proximity'

# Ensure working directory exists
os.makedirs(working_directory, exist_ok=True)

# Define input and output file paths within the working directory
input_file = os.path.join(working_directory, 'sample_data.csv')
output_file = os.path.join(working_directory, 'result_dataframe.csv')

# Check if input file exists
if not os.path.isfile(input_file):
    raise FileNotFoundError(f"Input file not found: {input_file}")

# Load data
data = pd.read_csv(input_file)

# Ensure necessary columns are present
required_columns = {'mmsi', 'lat', 'lon', 'timestamp'}
if not required_columns.issubset(data.columns):
    raise ValueError(f"Input data must contain the following columns: {required_columns}")

# Sort data by timestamp
data.sort_values('timestamp', inplace=True)

# Define proximity threshold (in kilometers)
threshold_value = 0.5

# Create a function to find proximity events
def find_proximity_events(data, threshold_value):
    results = []
    
    # Group data by timestamp
    collect = data.groupby('timestamp')
    
    for timestamp, arr in collect:
        arr = arr.reset_index(drop=True)
        coords = arr[['lat', 'lon']].to_numpy()
        mmsi = arr['mmsi'].to_numpy()
        
        tree = cKDTree(coords)
        pairs = tree.query_pairs(threshold_value / 6371.0, output_type='ndarray')  # Convert km to radians
        
        for i, j in pairs:
            dist = haversine(arr.loc[i, 'lat'], arr.loc[i, 'lon'], arr.loc[j, 'lat'], arr.loc[j, 'lon'])
            if dist <= threshold_value:
                results.append({
                    'mmsi': mmsi[i],
                    'vessel_proximity': mmsi[j],
                    'timestamp': timestamp
                })
                results.append({
                    'mmsi': mmsi[j],
                    'vessel_proximity': mmsi[i],
                    'timestamp': timestamp
                })
    
    return pd.DataFrame(results)

# Find proximity events
proximity_events = find_proximity_events(data, threshold_value)

# Group by MMSI and timestamp to list interacting vessels
final_results = proximity_events.groupby(['mmsi', 'timestamp'])['vessel_proximity'].apply(list).reset_index()

# Print debug information
print(f"Working directory: {working_directory}")
print(f"Output file path: {output_file}")
print("Final results preview:")
print(final_results.head())

# Save results to a CSV file with exception handling
try:
    final_results.to_csv(output_file, index=False)
    print(f"Results successfully saved to {output_file}")
except Exception as e:
    print(f"Error saving results to file: {e}")