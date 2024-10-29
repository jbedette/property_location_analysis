from sklearn.cluster import DBSCAN
import numpy as np

# Sample data: each entry is a [latitude, longitude] coordinate
data = np.array([[lat1, lon1], [lat2, lon2], ...])

# DBSCAN parameters: adjust epsilon and min_samples as needed
db = DBSCAN(eps=0.1, min_samples=5).fit(data)

# Extract cluster labels
labels = db.labels_

# Cluster labels are -1 for noise points, or a cluster ID for each point
clusters = [data[labels == i] for i in set(labels) if i != -1]
noise = data[labels == -1]
