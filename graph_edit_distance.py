"""
Graph edit distance functions
"""

import numpy as np
from typing import Callable


def HammingDistance(cell_a: np.array, cell_b: np.array) -> np.int32:
    return np.sum(np.abs(cell_a - cell_b))


def NASWOTDistance(cell_a: np.array, cell_b: np.array) -> np.int32:
    pass


def get_edit_distance_function(func: str = "Hamming") -> Callable:

    if func == "Hamming":
        return HammingDistance
    elif func == "NASWOT":
        return NASWOTDistance
    else:
        raise NotImplementedError(
            f"Unrecognised distance function: {func}. Options are: [Hamming, NASWOT]."
        )
