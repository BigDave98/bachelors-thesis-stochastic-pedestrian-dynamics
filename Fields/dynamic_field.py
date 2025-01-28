import numpy as np


class DynamicField:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.dynamic_field = np.zeros((width, height))

    def __getitem__(self, position):
        """Permite acessar o grid usando grid[y,x]"""
        return self.dynamic_field[position]

    def __setitem__(self, position, value):
        """Permite modificar o grid usando grid[y,x] = value"""
        self.dynamic_field[position] = value

    def decay(self):
        if np.any(self.dynamic_field > 5):
           self.dynamic_field /= 2

    def update_dynamic_field(self, positions):
        self.dynamic_field[tuple(zip(*positions))] += 1
        self.decay()

    def get_neighbors_matrix(self, position):
        """
        Retorna uma matriz 3x3 com os valores ao redor da posição.

        Args:
            matriz: A matriz original
            posicao: Tupla (y, x) com a posição central

        Returns:
            Matriz 3x3 numpy com os valores vizinhos
        """
        y, x = position
        neighbors = np.zeros((3, 3))

        for j in range(3):
            for i in range(3):
                # Calcula a posição real na matriz original
                pos_y = y + (i - 1)  # -1, 0, 1
                pos_x = x + (j - 1)  # -1, 0, 1

                # Verifica se a posição é válida na matriz original
                if 0 <= pos_y < self.height and 0 <= pos_x < self.width:
                    neighbors[i, j] = self.dynamic_field[pos_y, pos_x]

        neighbors[1, 1] = 0

        return neighbors