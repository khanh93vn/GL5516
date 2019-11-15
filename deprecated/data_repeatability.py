import glob
import numpy as np
import pandas as pd

# Declare paths
input_paths = "raw_data/at_*"
output_path = "processed_data/repeatability.csv"

# Get file names:
file_names = glob.glob(input_paths)

# Get labels:
labels = [int(file_name.split('_')[-1]) for file_name in file_names]

# Get files:
data = [np.fromfile(file_name) for file_name in file_names]

# Build data-frame:
df = pd.DataFrame(dict(zip(labels, data))).sort_index(axis=1)

# Save data-frame:
df.to_csv(output_path, index=False)

# -----------------------------------------------------------------------------