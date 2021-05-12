import numpy as np
import pandas as pd

from tqdm import tqdm


df: pd.DataFrame = pd.read_pickle("minibench/minibench-arch-cell-accs-matrix.pd")
distance_matrix: np.array = np.zeros((15625, 15625), dtype=np.int32)


def compute_edit_distance(cell_a: np.array, cell_b: np.array) -> np.int32:
    return np.sum(np.abs(cell_a - cell_b))


for i, cell_a in tqdm(df.iterrows()):
    for j, cell_b in df.iterrows():
        distance_matrix[i, j] = compute_edit_distance(
            cell_a["matrix"], cell_b["matrix"]
        )

np.save("minibench_nasbench201_distance_matrix.npy", distance_matrix)