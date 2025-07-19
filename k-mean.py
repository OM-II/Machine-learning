from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

# Sample data
X = np.array([[1,2], [1,4], [1,0],
              [4,2], [4,4], [4,0]])

# Apply KMeans with 2 clusters
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)

# Cluster centers
print("Centroids:\n", kmeans.cluster_centers_)

# Cluster labels
print("Labels:\n", kmeans.labels_)

# Plotting
plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_)
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], color='red', marker='X')
plt.title("K-Means Clustering")
plt.show()
