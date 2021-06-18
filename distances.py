import argparse
import numpy as np
import pandas as pd

from tqdm import tqdm
from graph_edit_distance import get_edit_distance_function
from typing import Callable


parser = argparse.ArgumentParser(
    description="Compute a 15625x15625 adj_matrix of distances."
)
parser.add_argument("--edit_distance_function", default="Hamming", type=str)
args: argparse.Namespace = parser.parse_args()

df: pd.DataFrame = pd.read_pickle("minibench/minibench-arch-cell-accs-matrix.pd")
distance_matrix: np.array = np.zeros((1000, 1000), dtype=np.int32)

compute_edit_distance: Callable = get_edit_distance_function(
    args.edit_distance_function
)

for i, cell_a in tqdm(df.iterrows()):
    if i >= 1000:
        break

    for j, cell_b in df.iterrows():
        if j >= 1000:
            break

        distance_matrix[i, j] = compute_edit_distance(
            cell_a["matrix"], cell_b["matrix"]
        )

np.save("minibench_nasbench201_distance_matrix.npy", distance_matrix)
