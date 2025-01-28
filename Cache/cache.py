from PathFinding import find_path_cong

class Cache:
    def __init__(self):
        self.path_cache = {}
        self.cost_cache = {}

    def cache_path(self, pedestrian, exit, grid):
        """Armazena caminhos já calculados para evitar recálculos."""
        cache_key = (pedestrian.position, exit)
        if cache_key not in self.path_cache:
            self.path_cache[cache_key] = find_path_cong(grid, pedestrian.position, exit)

        return self.path_cache[cache_key]

    def clear_cache(self):
        self.path_cache.clear()