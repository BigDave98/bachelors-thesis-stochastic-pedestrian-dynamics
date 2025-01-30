from typing import Tuple, List
import numpy as np
from numpy.typing import NDArray

# Grid dimensions
width: int = 50
height: int = 50

is_rooms = False

num_pedestrians = 100

# Exit positions: (left wall, top exit, right wall)
exits = ((30, 0),  #left wall
          (height-1, width//2),  # Top exit
          (30,49) #right wall
)

# Preference matrix for movement decisions
preference_matrix: List[List[float]] = [
    [0.055, 0.85, 0.055],
    [0.01, 0, 0.01],
    [0.007, 0.006, 0.007]
]

# Possible movement directions (relative positions)
moves: List[List[Tuple[int, int]]] = [
   [(-1, -1), (-1,  0), (-1,  1)],
   [( 0, -1), ( 0,  0), ( 0,  1)],
   [( 1, -1), ( 1,  0), ( 1,  1)]
]

# All possible movement directions (orthogonal and diagonal)
directions: List[Tuple[int, int]] = [
   # Orthogonal movements
   (0,  1), (0, -1), (1,  0), (-1,  0),
   # Diagonal movements
   (1,  1), (1, -1), (-1, 1), (-1, -1)
]


def get_min_max(
        position: Tuple[int, int],
        grid: NDArray,
        radius: int
) -> Tuple[int, int, int, int]:
    """
    Calculate boundary indices for a neighborhood around a position.

    Args:
        position: Center position (y, x)
        grid: Environment grid
        radius: Radius of neighborhood

    Returns:
        Tuple containing:
            - y_min: Minimum y coordinate
            - y_max: Maximum y coordinate
            - x_min: Minimum x coordinate
            - x_max: Maximum x coordinate

    Note:
        Ensures returned indices are within grid boundaries
    """
    y, x = position
    y_min = max(0, y - radius)
    y_max = min(grid.shape[0], y + radius + 1)
    x_min = max(0, x - radius)
    x_max = min(grid.shape[1], x + radius + 1)

    return y_min, y_max, x_min, x_max