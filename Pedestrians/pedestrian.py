from heapq import heappush, heappop
import numpy as np
import PathFinding
import random


class Pedestrian:
    def __init__(self):
        self.id = 0
        self.position = None
        self.prefered_move = None
        self.prefered_next_position = None
        self.chosen_exit = None


    def is_near_exit(self, radius=3):
        """
        Verifica se a posição está próxima à saída.
        """
        y, x = self.position
        exit_y, exit_x = self.chosen_exit

        # Verifica se o pedestre está a um raio de 4 celulas da saida, se sim retorna true, cc false
        return abs(y - exit_y) <= radius and abs(x - exit_x) <= radius

    def get_possible_moves(self, width, height, moves, grid, center_x = 1, center_y = 1):
        possible_moves = np.zeros((3, 3), dtype=object)
        cell_position = list(self.position)

        for line in moves:
            for move in line:
                new_pos = [cell_position[0] + move[0], cell_position[1] + move[1]]
                pos_x = center_x + move[0]
                pos_y = center_y + move[1]

                # Verifica se o movimento é válido (dentro do grid e não é parede)
                if (0 <= new_pos[0] < height and
                        0 <= new_pos[1] < width and
                        grid[new_pos[0], new_pos[1]] != 3):  # Verifica se não é parede
                    possible_moves[pos_x, pos_y] = move
                else:
                    possible_moves[pos_x, pos_y] = None

        return possible_moves

    @staticmethod
    def chose_next_move(rotated_preference_matrix, moves):
        moves_ = []
        for line in moves:
            for move in line:
                moves_.append(move)
        next_move = random.choices(moves_, np.array(rotated_preference_matrix).flatten())
        return next_move



    def get_neighbors(self, grid):
        """Retorna as células vizinhas válidas evitando paredes."""
        rows, cols = grid.height, grid.width
        neighbors = []

        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # ortogonais
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # diagonais
        ]

        for dy, dx in directions:
            new_y, new_x = self[0] + dy, self[1] + dx
            if 0 <= new_y < rows and 0 <= new_x < cols and grid[new_y, new_x] != 3:  # Verifica se não é parede
                neighbors.append((new_y, new_x))

        return neighbors



    def is_in_room(self, rooms_info):
        """
        Verifica se uma posição está dentro de algum quarto e retorna a posição da porta.
        Args:
            position: Tupla (y, x) com a posição do pedestre
            rooms_info: Lista de dicionários com informações dos quartos
        Returns:
            Tupla (True/False, door_position)
            - True e posição da porta se estiver em algum quarto
            - False e None se não estiver em nenhum quarto ou estiver na porta
        """
        y, x = self.position

        for room in rooms_info:
            start_y, start_x = room['start']
            end_y, end_x = room['end']

            # Se estiver na porta, considera como fora do quarto
            if self.position == room['door']:
                return False, None

            # Verifica se está dentro dos limites do quarto
            if start_y <= y < end_y and start_x <= x < end_x:
                return True, room['door']

        return False, None

    @staticmethod
    def find_path_cong(grid, start, goal):
        """Implementa o algoritmo A* com evitação de congestionamento."""
        open_set = [(0, start)]
        came_from = {}

        g_score = {start: 0}
        f_score = {start: PathFinding.euclidean_distance(start, goal)}

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

                tentative_g_score = g_score[current] + PathFinding.get_movement_cost(True, current, neighbor, grid)

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + PathFinding.euclidean_distance(neighbor, goal)
                    heappush(open_set, (f_score[neighbor], neighbor))

        return []








