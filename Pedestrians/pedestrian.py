import numpy as np
import random
from utils import directions


class Pedestrian:
    def __init__(self):
        self.id = 0
        self.position = None
        self.prefered_move = None
        self.best_move = None
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
    def is_in_room(self, rooms_info):
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

    def get_neighbors(self, grid):
        """Retorna as células vizinhas válidas evitando paredes."""
        rows, cols = grid.height, grid.width
        neighbors = []

        for dy, dx in directions:
            new_y, new_x = self[0] + dy, self[1] + dx
            if (0 <= new_y < rows and 0 <= new_x < cols and grid[new_y, new_x] != 3):  # Verifica se não é parede
                neighbors.append((new_y, new_x))

        return neighbors

    def get_possible_moves(self, width, height, moves, grid, center_x = 1, center_y = 1):
        possible_moves = np.zeros((3, 3), dtype=object)
        cell_position = list(self.position)

        for line in moves:
            for move in line:
                new_pos =  tuple(a + b for a, b in zip(cell_position, move))
                pos_x = center_x + move[0]
                pos_y = center_y + move[1]

                # Verifica se o movimento é válido (dentro do grid e não é parede)
                if (0 <= new_pos[0] < height and 0 <= new_pos[1] < width and grid[new_pos[0], new_pos[1]] != 3):  # Verifica se não é parede
                    possible_moves[pos_x, pos_y] = move

                else:
                    possible_moves[pos_x, pos_y] = None

        return possible_moves

    def get_best_move(self, path):
        if len(path) > 1:
            p1 = self.position
            p2 = path[1]

            self.best_move = tuple(b - a for a, b in zip(p1, p2))

    @staticmethod
    def chose_next_move(rotated_preference_matrix, moves):
        moves_ = []
        for line in moves:
            for move in line:
                moves_.append(move)

        probs = np.array(rotated_preference_matrix).flatten()
        next_move = random.choices(moves_, probs)

        return next_move

    def get_move(self, matrix, possible_moves):
        move_null = True
        while move_null:
            # Retorna o proximo movimento baseado na matriz de preferencias:
            self.prefered_move = self.chose_next_move(matrix, possible_moves)[0]

            if self.prefered_move != None:
                move_null = False





