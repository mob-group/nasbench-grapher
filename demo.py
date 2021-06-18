import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.colors as colors
import matplotlib.cm as cmx
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Generating sample data

adjacency_matrix = nx.from_numpy_matrix(
    np.load("minibench_nasbench201_distance_matrix.npy")
)

print(adjacency_matrix)

df: pd.DataFrame = pd.read_pickle("minibench/mini-bench-arch-cell-accs.pd")


df

fig, ax = plt.subplots()



accuracies = []
for i in range(1000):
    accuracies.append(df.iloc[i]["cifar10-test"])

options = {
    "node_color": accuracies,
    "node_size": 20,
    "edge_color": "white",
    "linewidths": 0,
    "width": 0.1,
}

nx.draw(adjacency_matrix, **options, ax=ax)

vmin = min(accuracies)
vmax = max(accuracies)
scalar_map = cmx.ScalarMappable(
    cmap=plt.get_cmap("viridis"), norm=plt.Normalize(vmin=vmin, vmax=vmax)
)
scalar_map.set_array([])
plt.colorbar(scalar_map)

plt.axis("equal")
plt.show()
