from heapq import heappush, heappop
from Pedestrians.pedestrian import Pedestrian
import numpy as np


def euclidean_distance(p1, p2):
    #Calcula a distância euclidiana entre dois pontos.
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def check_congestion(grid, position, threshold=3, radius=2):
   """
   Verifica se há congestionamento ao redor de uma posição.

   Args:
       grid: Matriz do ambiente
       position: Tupla (y, x) da posição atual
       threshold: Número de células ocupadas para considerar congestionamento
       radius: Raio para verificar vizinhança

   Returns:
       True se número de células ocupadas > threshold
   """
   y, x = position
   y_min = max(0, y - radius)
   y_max = min(grid.shape[0], y + radius + 1)
   x_min = max(0, x - radius)
   x_max = min(grid.shape[1], x + radius + 1)

   # Conta células ocupadas (valor 1) na vizinhança
   occupied_cells = np.sum(grid[y_min:y_max, x_min:x_max] == 1)

   return bool(occupied_cells > threshold)


def get_movement_cost(congestion, current, neighbor, grid):
    """Calcula o custo do movimento considerando paredes."""
    if grid[neighbor] == 3:  # Se for parede, custo infinito
        return float('inf')

    dy = abs(current[0] - neighbor[0])
    dx = abs(current[1] - neighbor[1])

    base_cost = 1.4 if dx and dy else 1.0
    congestion_cost = 0

    if congestion:
        radius = 2  # raio para verificar congestionamento
        y, x = neighbor
        y_min, y_max = max(0, y - radius), min(grid.height, y + radius + 1)
        x_min, x_max = max(0, x - radius), min(grid.width, x + radius + 1)

        neighborhood = grid[y_min:y_max, x_min:x_max]
        occupied_cells = np.sum(neighborhood == 1)

        # Aumenta o custo baseado no número de células ocupadas
        congestion_cost = occupied_cells * 0.7  # POsso adicionar um multiplicador


    return base_cost + congestion_cost


def get_movement_cost_cong(current, neighbor, grid):

   #Calcula o custo do movimento considerando paredes"""
   if grid[neighbor] == 3:  # Se for parede, custo infinito
       return float('inf')

   #Calcula o custo do movimento considerando congestionamento."""
   dy = abs(current[0] - neighbor[0])
   dx = abs(current[1] - neighbor[1])

   base_cost = 1.4 if dx and dy else 1.0

    # Adiciona custo extra baseado na densidade de células ao redor
   radius = 2  # raio para verificar congestionamento
   y, x = neighbor
   y_min, y_max = max(0, y - radius), min(grid.height, y + radius + 1)
   x_min, x_max = max(0, x - radius), min(grid.width, x + radius + 1)

   neighborhood = grid[y_min:y_max, x_min:x_max]
   occupied_cells = np.sum(neighborhood == 1)

    # Aumenta o custo baseado no número de células ocupadas
   congestion_cost = occupied_cells * 0.7 #POsso adicionar um multiplicador

   return base_cost + congestion_cost

def find_path(grid, start, goal):
    """Implementa o A* evitando paredes."""
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
            # Pula se for parede
            if grid[neighbor] == 3:
                continue

            tentative_g_score = g_score[current] + get_movement_cost(False, current, neighbor, grid)

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + euclidean_distance(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))

    return []


def get_path(congestion, near_exit, pedestrian, exit, selected_static_field, cache, grid):
    if (congestion and not near_exit):
        path = cache.cache_path(pedestrian, exit, grid)
    else:
        path = selected_static_field['path']

    return path

def find_path_cong(grid, start, goal):
    """Implementa o algoritmo A* com evitação de congestionamento."""
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
            # Pula se for parede
            if grid[neighbor] == 3:
                continue

            tentative_g_score = g_score[current] + get_movement_cost(True, current, neighbor, grid)

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + euclidean_distance(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))

    return []

def find_shortest_path(grid, exit, start):
   """
   Encontra o caminho mais curto do ponto inicial até a saida(2).
   """
   data = {'initial position': start,
           'exit': exit,
           'path': None,
           'steps': 0}

   data['path'] = find_path(grid, start, exit)
   data['steps'] = len(data['path'])

   return data