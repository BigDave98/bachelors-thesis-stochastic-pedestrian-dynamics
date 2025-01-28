from utils import preference_matrix
import numpy as np
import random

class PreferenceMatrix:
    def __init__(self):
        self.matrix = preference_matrix

    def __getitem__(self, position):
        """Permite acessar o grid usando grid[y,x]"""
        return self.matrix[position]

    def rotate_matrix(self, move):
        # Mapeia cada ângulo para sua rotação específica
        rotations = {
            (-1, -1): [  # 45 ok
                [self.matrix[0][1], self.matrix[0][2], self.matrix[1][2]],
                [self.matrix[0][0], self.matrix[1][1], self.matrix[2][2]],
                [self.matrix[1][0], self.matrix[2][0], self.matrix[2][1]]
            ],

            (0, -1): lambda m: np.rot90(m, k=1),  # 90,

            (1, -1): [  # 135 ok
                [self.matrix[1][2], self.matrix[2][2], self.matrix[2][1]],
                [self.matrix[0][2], self.matrix[1][1], self.matrix[2][0]],
                [self.matrix[0][1], self.matrix[0][0], self.matrix[1][0]]
            ],

            (1, 0): lambda m: np.rot90(m, k=2),  # 180

            (1, 1): [  # 225
                [self.matrix[2][1], self.matrix[2][0], self.matrix[1][0]],
                [self.matrix[2][2], self.matrix[1][1], self.matrix[0][0]],
                [self.matrix[1][2], self.matrix[0][2], self.matrix[0][1]]
            ],

            (0, 1): lambda m: np.rot90(m, k=3),  # 270

            (-1, 1): [  # 315
                [self.matrix[1][0], self.matrix[0][0], self.matrix[0][1]],
                [self.matrix[2][0], self.matrix[1][1], self.matrix[0][2]],
                [self.matrix[2][1], self.matrix[2][2], self.matrix[1][2]]
            ],
            (-1, 0): self.matrix  # original

            , (0, 0): self.matrix

        }

        if move in [(0, -1), (1, 0), (0, 1)]:
            return rotations[move](self.matrix)

        else:
            return rotations[move]

    def normalize_matrix(self):
        """
        Normaliza os valores da matriz para que a soma total seja 1.

        Args:
            matriz: Matriz numpy para normalizar

        Returns:
            Matriz normalizada onde a soma de todos os elementos é 1
        """
        # Evita divisão por zero
        if np.sum(self.matrix) == 0:
            self.matrix

        self.matrix /= np.sum(self.matrix)

    def chose_next_move(self, moves):
        moves_ = []
        for line in moves:
            for move in line:
                moves_.append(move)
        next_move = random.choices(moves_, np.array(self.matrix).flatten())
        return next_move

    def get_matrix(self, prefered_next_move, dynamic_field_neighbors):
        self.matrix = self.rotate_matrix(prefered_next_move)
        # Calcula os valores da matriz de preferencias levando em conta o static e o dynamic Fields
        self.matrix = np.exp(dynamic_field_neighbors) * np.exp(np.array(self.matrix) * 5)
        # Normaliza a matriz de preferencia para que a soma das probabilidades presentes nela nunca seja maior do que 1
        self.normalize_matrix()
