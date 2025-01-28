from PathFinding import find_path

class Cache:
    def __init__(self):
        self.path_cache = {}
        self.cost_cache = {}

    def cache_path(self, pedestrian, exit, grid):
        """Armazena caminhos já calculados para evitar recálculos."""
        cache_key = (pedestrian.position, exit)
        if cache_key not in self.path_cache:
            self.path_cache[cache_key] = find_path(grid, pedestrian.position, exit, True)

        return self.path_cache[cache_key]

    def clear_cache(self, steps):
        if steps % 3 == 0 and steps != 0:
            self.path_cache.clear()