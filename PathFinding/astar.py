from typing import Dict, List, Tuple, Optional, Any
from heapq import heappush, heappop
from Pedestrians.pedestrian import Pedestrian
from utils import get_min_max
import numpy as np
from numpy.typing import NDArray

Position = Tuple[int, int]
Path = List[Position]
GridType = NDArray[np.int_]

def euclidean_distance(p1: Position, p2: Position) -> float:
    """
    Calculate the Euclidean distance between two points.

    Args:
        p1: First point as (y, x) coordinates
        p2: Second point as (y, x) coordinates

    Returns:
        float: Euclidean distance between the points
    """
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def check_congestion(
    grid: GridType,
    position: Position,
    threshold: int = 3,
    radius: int = 2
) -> bool:
   """
   Check if there is congestion around a position.

    Args:
        grid: Environment matrix
        position: Current position as (y, x) tuple
        threshold: Number of occupied cells to consider congestion
        radius: Radius to check neighborhood

    Returns:
        bool: True if number of occupied cells > threshold
   """
   y_min, y_max, x_min, x_max = get_min_max(position, grid, radius)

   occupied_cells = np.sum(grid[y_min:y_max, x_min:x_max] == 1)

   return bool(occupied_cells > threshold)


def get_movement_cost(
    congestion: bool,
    current: Position,
    neighbor: Position,
    grid: GridType,
    radius: int = 2
) -> float:
    """
    Calculate movement cost considering walls and congestion.

    Args:
        congestion: Whether to consider congestion in cost calculation
        current: Current position as (y, x)
        neighbor: Neighbor position as (y, x)
        grid: Environment matrix

    Returns:
        float: Movement cost (infinity for walls)
    """
    if grid[neighbor] == 3:  # Wall
        return float('inf')

    dy = abs(current[0] - neighbor[0])
    dx = abs(current[1] - neighbor[1])

    base_cost = 1.4 if dx and dy else 1.0
    congestion_cost = 0

    if congestion:
        y_min, y_max, x_min, x_max = get_min_max(neighbor, grid, radius)

        neighborhood = grid[y_min:y_max, x_min:x_max]
        occupied_cells = np.sum(neighborhood == 1)


        congestion_cost = occupied_cells * 0.7

    return base_cost + congestion_cost

def find_path(
    grid: GridType,
    start: Position,
    goal: Position,
    consider_congestion: bool
) -> Path:
    """
    Implement A* pathfinding avoiding walls.

    Args:
        grid: Environment matrix
        start: Starting position as (y, x)
        goal: Goal position as (y, x)
        consider_congestion: Whether to consider congestion in pathfinding

    Returns:
        List of positions representing the path from start to goal.
        Empty list if no path is found.
    """
    open_set = [(0, start)]
    came_from = {}

    g_score = {start: 0}
    f_score = {start: euclidean_distance(start, goal)}

    while open_set:
        current = heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in Pedestrian.get_neighbors(current, grid):
            # Skip if it's a wall
            if grid[neighbor] == 3:
                continue

            tentative_g_score = g_score[current] + get_movement_cost(consider_congestion, current, neighbor, grid.grid)

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + euclidean_distance(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))

    return []

def find_shortest_path(
    grid: GridType,
    exit: Position,
    start: Position
) -> Dict[str, Any]:
   """
   Find the shortest path from starting point to exit.

    Args:
        grid: Environment matrix
        exit: Exit position as (y, x)
        start: Starting position as (y, x)

    Returns:
        Dictionary containing:
            - 'initial position': Starting position
            - 'exit': Exit position
            - 'path': List of positions representing the path
            - 'steps': Number of steps in the path
   """
   data = {'initial position': start,
           'exit': exit,
           'path': None,
           'steps': 0}

   data['path'] = find_path(grid, start, exit, False)
   data['steps'] = len(data['path'])

   return data


def get_path(
    congestion: bool,
    near_exit: bool,
    pedestrian: Pedestrian,
    exit: Position,
    selected_static_field: Dict[str, Any],
    cache: Any,
    grid: GridType
) -> Path:
    """
    Get appropriate path based on congestion and proximity to exit.

    Args:
        congestion: Whether there is congestion
        near_exit: Whether pedestrian is near exit
        pedestrian: Pedestrian object
        exit: Exit position
        selected_static_field: Dictionary containing static field information
        cache: Cache object for path storage
        grid: Environment matrix

    Returns:
        List of positions representing the path
    """
    if (congestion and not near_exit):
        path = cache.cache_path(pedestrian, exit, grid)
    else:
        path = selected_static_field['path']

    return path

