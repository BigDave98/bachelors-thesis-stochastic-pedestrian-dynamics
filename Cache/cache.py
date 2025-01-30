from typing import Dict, List, Tuple, Any
from PathFinding import find_path
from numpy.typing import NDArray

Position = Tuple[int, int]
CacheKey = Tuple[Position, Position]
Path = List[Position]


class Cache:
    """
    Caches pathfinding results to improve performance.

    This class implements a caching system for pathfinding results to avoid
    recalculating paths that have been previously computed. It also includes
    a periodic cache clearing mechanism to prevent memory bloat.

    Attributes:
        path_cache (Dict[CacheKey, Path]): Stores computed paths
        cost_cache (Dict): Stores computed costs (currently unused)
    """

    def __init__(self) -> None:
        """Initialize empty path and cost caches."""
        self.path_cache: Dict[CacheKey, Path] = {}
        self.cost_cache: Dict = {}  # Reserved for future use

    def cache_path(self, pedestrian: Any, exit: Position, grid: NDArray) -> Path:
        """
        Cache and retrieve pathfinding results.

        Checks if a path has been previously calculated for the given
        start and end positions. If not, calculates and caches the new path.

        Args:
            pedestrian: Pedestrian object containing current position
            exit: Exit position (y, x)
            grid: Environment grid

        Returns:
            List of positions representing the path to the exit

        Note:
            Uses pedestrian's current position and exit position as cache key
        """
        cache_key = (pedestrian.position, exit)
        if cache_key not in self.path_cache:
            self.path_cache[cache_key] = find_path(grid, pedestrian.position, exit, True)

        return self.path_cache[cache_key]

    def clear_cache(self, steps: int) -> None:
        """
        Periodically clear the path cache to prevent memory bloat.

        Args:
            steps: Current simulation step count

        Note:
            Clears cache every 3 steps (when steps % 3 == 0),
            except at step 0
        """
        if steps % 3 == 0 and steps != 0:
            self.path_cache.clear()