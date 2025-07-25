import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

X, y = make_blobs(centers=3, cluster_std=0.5, random_state=0)

plt.scatter(X[:, 0], X[:, 1], c=y)
plt.title("Three normally-distributed clusters")
plt.show()