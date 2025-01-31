import numpy as np
from typing import List, Tuple
from numpy.typing import NDArray
from utils import kernel, delta, diffusion_coef
from scipy.ndimage import convolve

Position = Tuple[int, int]
Positions = List[Position]


class DynamicField:
    """
    Manages the dynamic floor field for pedestrian simulation.

    This class handles a dynamic field that tracks pedestrian movement history
    and influences future movement decisions through pheromone-like traces.

    Attributes:
        width (int): Width of the dynamic field
        height (int): Height of the dynamic field
        dynamic_field (NDArray): Matrix storing dynamic field values
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize dynamic field with given dimensions.

        Args:
            width: Width of the field
            height: Height of the field
        """
        self.width = width
        self.height = height
        self.dynamic_field: NDArray = np.zeros((width, height))

    def __getitem__(self, position: Position) -> float:
        """
        Enable field access using field[y,x] syntax.

        Args:
            position: Tuple of (y, x) coordinates

        Returns:
            Value at the specified position
        """
        return self.dynamic_field[position]

    def __setitem__(self, position: Position, value: float) -> None:
        """
        Enable field modification using field[y,x] = value syntax.

        Args:
            position: Tuple of (y, x) coordinates
            value: Value to set at the position
        """
        self.dynamic_field[position] = value

    def decay_and_diffuse(self) -> None:
        # Apply Diffusion
        diffused = convolve(self.dynamic_field , kernel)

        # Aply decay
        self.dynamic_field = self.dynamic_field  * (1 - delta)

        # Function (7) from C. Burstedde Article
        self.dynamic_field += (diffusion_coef * diffused)

        # Limita valores entre 0 e 1
        self.dynamic_field = np.clip(self.dynamic_field, 0, 1)

    def update_dynamic_field(self, positions: Positions) -> None:
        """
        Update dynamic field based on pedestrian positions.

        Args:
            positions: List of positions to update

        Note:
            Increments field value at each position and applies decay
        """
        self.dynamic_field[tuple(zip(*positions))] += 1
        self.decay_and_diffuse()

    def get_neighbors_matrix(self, position: Position) -> NDArray:
        """
        Get a 3x3 matrix of neighboring field values around a position.

        Args:
            position: Tuple (y, x) of center position

        Returns:
            3x3 numpy matrix containing neighboring values.
            The center value (current position) is set to 0.
            Out-of-bounds positions are set to 0.

        Note:
            For a position (y,x), returns values in this pattern:
            [[(y-1,x-1), (y-1,x), (y-1,x+1)],
             [(y,x-1),   (y,x),   (y,x+1)],
             [(y+1,x-1), (y+1,x), (y+1,x+1)]]
        """
        y, x = position
        neighbors = np.zeros((3, 3))

        for j in range(3):
            for i in range(3):
                # Calculate actual position in original matrix
                pos_y = y + (i - 1)  # -1, 0, 1
                pos_x = x + (j - 1)  # -1, 0, 1

                # Check if position is valid in original matrix
                if 0 <= pos_y < self.height and 0 <= pos_x < self.width:
                    neighbors[i, j] = self.dynamic_field[pos_y, pos_x]

        # Set center value to 0
        neighbors[1, 1] = 0

        return neighbors