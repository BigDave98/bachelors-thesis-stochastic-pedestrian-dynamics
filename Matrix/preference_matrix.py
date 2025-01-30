from typing import List, Tuple, Union, Any
from utils import preference_matrix
import numpy as np
from numpy.typing import NDArray
import random

MatrixType = NDArray[np.float64]
Move = Tuple[int, int]
Moves = List[List[Move]]


class PreferenceMatrix:
    """
    Manages preference matrices for pedestrian movement.

    This class handles the creation, rotation, and normalization of preference
    matrices that guide pedestrian movement decisions.

    Attributes:
        matrix (NDArray): The preference matrix for movement
    """
    def __init__(self) -> None:
        """Initialize preference matrix with default values."""
        self.matrix = preference_matrix

    def __getitem__(self, position: Tuple[int, ...]) -> Any:
        """
       Enable grid access using grid[y,x] syntax.

       Args:
           position: Index tuple for accessing the matrix

       Returns:
           Matrix value at the specified position
       """
        return self.matrix[position]

    def rotate_matrix(self, move: Move) -> MatrixType:
        """
        Rotate preference matrix based on movement direction.

        Args:
            move: Movement direction as (y, x) tuple

        Returns:
            Rotated preference matrix

        Note:
            Different rotations are applied based on movement angle:
            - (-1, -1): 45 degrees
            - (0, -1): 90 degrees
            - (1, -1): 135 degrees
            - (1, 0): 180 degrees
            - (1, 1): 225 degrees
            - (0, 1): 270 degrees
            - (-1, 1): 315 degrees
            - (-1, 0) or (0, 0): no rotation
        """
        # Map each angle to its specific rotation
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
            (-1, 0): self.matrix  # Original matrix

            , (0, 0): self.matrix # Original matrix

        }

        if move in [(0, -1), (1, 0), (0, 1)]:
            return rotations[move](self.matrix)

        else:
            return rotations[move]

    def normalize_matrix(self) -> None:
        """
        Normalize matrix values so their sum equals 1.

        Note:
            - Modifies the matrix in place
            - If sum is 0, returns without modification
        """
        # Avoid division by zero
        if np.sum(self.matrix) == 0:
            self.matrix

        self.matrix /= np.sum(self.matrix)

    def chose_next_move(self, moves: Moves) -> List[Move]:
        """
        Choose next move based on preference matrix probabilities.

        Args:
            moves: List of possible moves

        Returns:
            Selected move based on preference matrix probabilities
        """
        moves_ = []
        for line in moves:
            for move in line:
                moves_.append(move)
        next_move = random.choices(moves_, np.array(self.matrix).flatten())
        return next_move

    def get_matrix(
            self,
            prefered_next_move: Move,
            dynamic_field_neighbors: MatrixType
    ) -> None:
        """
        Update preference matrix based on preferred move and dynamic field.

        Args:
            prefered_next_move: Preferred movement direction
            dynamic_field_neighbors: Dynamic field values for neighboring cells

        Note:
            - Rotates matrix based on preferred movement
            - Combines static and dynamic field influences
            - Normalizes final matrix
        """
        # Rotate matrix based on preferred movement
        self.matrix = self.rotate_matrix(prefered_next_move)

        # Calculate preference matrix values considering static and dynamic fields
        self.matrix = np.exp(dynamic_field_neighbors) * np.exp(np.array(self.matrix) * 5)

        # Normalize preference matrix so probability sum never exceeds 1
        self.normalize_matrix()
