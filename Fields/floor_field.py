import numpy as np
import random
from typing import List, Tuple
from Pedestrians import Pedestrian


class FloorField:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.grid = np.zeros((width, height))

    def __getitem__(self, position):
        """Permite acessar o grid usando grid[y,x]"""
        return self.grid[position]

    def __setitem__(self, position, value):
        """Permite modificar o grid usando grid[y,x] = value"""
        self.grid[position] = value

    def add_exit(self, exits: Tuple[Tuple]) -> None:
        for exit_coordinates in exits:
            self.grid[exit_coordinates] = 2

    def add_walls(self, start_pos, size, door_pos):
        y, x = start_pos
        h, w = size

        # Adiciona paredes
        self.grid[y:y + h, x] = 3  # Parede esquerda
        self.grid[y:y + h, x + w - 1] = 3  # Parede direita
        self.grid[y, x:x + w] = 3  # Parede superior
        self.grid[y + h - 1, x:x + w] = 3  # Parede inferior

        # Adiciona porta
        door_y, door_x = door_pos
        self.grid[door_y, door_x] = 0

    def setup_rooms(self):
        """
        Cria 3 quartos nas posições especificadas e retorna suas informações.

        Returns:
            grid: Grid atualizado com os quartos
            rooms_info: Lista de dicionários com informações dos quartos
        """
        rooms_info = []

        # Quarto 1: Inferior Esquerdo
        room1_start = (self.height - 15, 5)
        room1_size = (15, 15)
        door1_pos = (self.height - 15, 12)
        self.add_walls(room1_start, room1_size, door1_pos)

        rooms_info.append({
            'start': room1_start,
            'end': (room1_start[0] + room1_size[0], room1_start[1] + room1_size[1]),
            'door': door1_pos
        })

        # Quarto 2: Inferior Direito
        room2_start = (self.height - 15, 30)
        room2_size = (15, 20)
        door2_pos = (self.height - 15, 40)
        self.add_walls(room2_start, room2_size, door2_pos)

        rooms_info.append({
            'start': room2_start,
            'end': (room2_start[0] + room2_size[0], room2_start[1] + room2_size[1]),
            'door': door2_pos
        })

        # Quarto 3: Superior Central
        room3_start = (0, 10)
        room3_size = (25, 20)
        door3_pos = (24, 20)
        self.add_walls(room3_start, room3_size, door3_pos)

        rooms_info.append({
            'start': room3_start,
            'end': (room3_start[0] + room3_size[0], room3_start[1] + room3_size[1]),
            'door': door3_pos
        })

        return rooms_info

    def available_positions(self, num_pedestrians):
        # Verifica as coordenadas que estão livres no grid para posicionar os pedestres
        available_positions = [(i, j) for i in range(self.height) for j in range(self.width) if self.grid[i, j] == 0]

        return available_positions

    def set_pedestrians(self, pedestrians, num_pedestrians):
        avaliable_positions = self.available_positions(num_pedestrians)
        positions = random.sample(avaliable_positions, num_pedestrians)

        for idx, position in enumerate(positions):
            pedestrian = Pedestrian()
            pedestrian.id = idx
            pedestrian.position = position

            self.grid[position] = 1

            pedestrians.info.append(pedestrian)
            pedestrians.positions.append(pedestrian.position)

        return pedestrians.info

    def check_congestion(self, position, threshold=3, radius=2):
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
        y_max = min(self.grid.shape[0], y + radius + 1)
        x_min = max(0, x - radius)
        x_max = min(self.grid.shape[1], x + radius + 1)

        # Conta células ocupadas (valor 1) na vizinhança
        occupied_cells = np.sum(self.grid[y_min:y_max, x_min:x_max] == 1)

        return bool(occupied_cells > threshold)


