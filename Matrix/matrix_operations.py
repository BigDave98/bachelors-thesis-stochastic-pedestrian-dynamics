import numpy as np
from numpy.typing import NDArray


def normalize_matrix(matrix: NDArray) -> NDArray:
    """
    Normalize the matrix values so that the total sum equals 1.

    Args:
        matrix: NumPy matrix to normalize

    Returns:
        Normalized matrix where the sum of all elements is 1

    Note:
        If the sum of the matrix is 0, returns the original matrix.
        Sets all elements with value 1 to 0 before normalization.
    """
    # Avoid division by zero
    if np.sum(matrix) == 0:
        return matrix

    matrix[matrix == 1] = 0

    return matrix / np.sum(matrix)