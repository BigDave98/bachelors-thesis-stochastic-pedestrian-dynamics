from config import preference_matrix
import numpy as np

class PreferenceMatrix:
    def __init__(self):
        self.matrix = preference_matrix

    def __getitem__(self, position):
        """Permite acessar o grid usando grid[y,x]"""
        return self.preference_matrix[position]

    def rotate_matrix(self, move):
        # Mapeia cada ângulo para sua rotação específica
        rotations = {
            (-1, -1): [  # 45 ok
                [preference_matrix[0][1], preference_matrix[0][2], preference_matrix[1][2]],
                [preference_matrix[0][0], preference_matrix[1][1], preference_matrix[2][2]],
                [preference_matrix[1][0], preference_matrix[2][0], preference_matrix[2][1]]
            ],

            (0, -1): lambda m: np.rot90(m, k=1),  # 90,

            (1, -1): [  # 135 ok
                [preference_matrix[1][2], preference_matrix[2][2], preference_matrix[2][1]],
                [preference_matrix[0][2], preference_matrix[1][1], preference_matrix[2][0]],
                [preference_matrix[0][1], preference_matrix[0][0], preference_matrix[1][0]]
            ],

            (1, 0): lambda m: np.rot90(m, k=2),  # 180

            (1, 1): [  # 225
                [preference_matrix[2][1], preference_matrix[2][0], preference_matrix[1][0]],
                [preference_matrix[2][2], preference_matrix[1][1], preference_matrix[0][0]],
                [preference_matrix[1][2], preference_matrix[0][2], preference_matrix[0][1]]
            ],

            (0, 1): lambda m: np.rot90(m, k=3),  # 270

            (-1, 1): [  # 315
                [preference_matrix[1][0], preference_matrix[0][0], preference_matrix[0][1]],
                [preference_matrix[2][0], preference_matrix[1][1], preference_matrix[0][2]],
                [preference_matrix[2][1], preference_matrix[2][2], preference_matrix[1][2]]
            ],
            (-1, 0): preference_matrix  # original

            , (0, 0): preference_matrix

        }

        if move in [(0, -1), (1, 0), (0, 1)]:
            return rotations[move](preference_matrix)

        else:
            return rotations[move]