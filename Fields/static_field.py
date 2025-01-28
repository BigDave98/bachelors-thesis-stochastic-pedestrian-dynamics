import random
from PathFinding import *
import numpy as np


class StaticField:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.static_field = np.zeros((width, height), dtype=object)

    def __getitem__(self, position):
        """Permite acessar o grid usando grid[y,x]"""
        x, y = position
        return self.static_field[x, y]

    def __setitem__(self, position, value):
        """Permite modificar o grid usando grid[y,x] = value"""
        x, y = position
        self.static_field[x, y] = value

    def set_static_field_ij(self, grid, position, exits):

        if self.static_field[position] == 0:
            static_fields_ij = []

            # Retorna os passos, posições e quantidade de pasos até a saida desejada
            for exit in exits:  # ((1,5), (9,5)) -> (1,5) (9,5)
                static_field_ij = find_shortest_path(grid, exit, position)
                static_fields_ij.append(static_field_ij)

            self.static_field[position] = static_fields_ij

    # Retorna as probabilidades para cada campo estático
    def prob_field_Sij(self, position, len_exits):  # i = linhas e j = colunas
        possible_steps_to_exit = list(map(lambda x: x['steps'], self.static_field[position]))
        sum_static_field_ij = sum(possible_steps_to_exit)

        probsSx = []
        probsSx_ = []
        # Prob da celula na posição (ij) ter o campo Sij(wp) como seu SF
        for i in range(len_exits):
            probSx = (1 / self.static_field[position][i]['steps'] / (1 / sum_static_field_ij))  # Função 3 do artigo
            probsSx.append(probSx)

        sum_probs = sum(probsSx)

        for i in probsSx:
            probSx_ = i / sum_probs
            probsSx_.append(probSx_)

        return list(probsSx_)

    def select_static_field(self, position, prob_field_sij):
        return random.choices(self.static_field[position], prob_field_sij)


    def get_static_field(self, inside_room, door_position, pedestrian, exits, grid):
        if inside_room:
            self.set_static_field_ij(grid, pedestrian.position, [door_position])

            if pedestrian.chosen_exit == None:
                selected_static_field = self.static_field[pedestrian.position][0]
                pedestrian.chosen_exit = selected_static_field['exit']
            else:
                selected_static_field = self.static_field[pedestrian.position][0]
        else:
            # Atribui valores ao static_field baseado na posição que o pedestre se encontra agora
            self.set_static_field_ij(grid, pedestrian.position, exits)

            # Calcula a prob para cada static field baseado na distancia até a saida
            prob = self.prob_field_Sij(pedestrian.position, len(exits))

            if pedestrian.chosen_exit == None or (pedestrian.chosen_exit not in exits and not inside_room):

                # Seleciona um dos static field baseado nas probabilidades
                selected_static_field = self.select_static_field(pedestrian.position, prob)[0]
                pedestrian.chosen_exit = selected_static_field['exit']

            else:
                selected_static_field = [field for field in self.static_field[pedestrian.position] if field['exit'] == pedestrian.chosen_exit][0]

        return selected_static_field, pedestrian


