import numpy as np

def normalize_matrix(matrix):
    """
    Normaliza os valores da matriz para que a soma total seja 1.

    Args:
        matriz: Matriz numpy para normalizar

    Returns:
        Matriz normalizada onde a soma de todos os elementos é 1
    """
    # Evita divisão por zero
    if np.sum(matrix) == 0:
        return matrix

    matrix[matrix == 1] = 0

    matriz_ = matrix / np.sum(matrix)

    return matrix / np.sum(matrix)