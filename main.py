from PathFinding import get_path
from config import *
from Fields import FloorField, DynamicField, StaticField
from Cache import Cache
from Pedestrians import Pedestrians
from animation import create_animation
from Matrix import PreferenceMatrix
import Matrix.matrix_operations as mo
import numpy as np

def main():
    steps = 0
    frames = []

    cache = Cache()

    #Inicia o grid com as saidas e quartos
    grid = FloorField(width, height)
    grid.add_exit(exits)
    rooms = grid.setup_rooms()


    #Instancia o dicionario que ira conter as informações dos pedestres e adiciona as informações da posição
    pedestrians_info = Pedestrians()
    pedestrians_info.info = grid.set_pedestrians(pedestrians_info, num_pedestrians)

    # Inicia o DynamicField
    dynamic_field = DynamicField(width, height)

    # Inicia o StaticField:
    static_field = StaticField(width, height)

    while pedestrians_info.info:
        pedestrians_info.prefered_next_positions, pedestrians_info.prefered_moves = [], []
        # Calcula a prob da proxima posição preferida para cada pedestre
        for pedestrian in pedestrians_info.info:
            # Verifica se esta dentro de um quarto, caso esteja retorna TRUE e a posição da porta em questão
            inside_room, door_position = pedestrian.is_in_room(rooms)

            selected_static_field, pedestrian = static_field.get_static_field(inside_room, door_position, pedestrian, exits, grid)

            exit = pedestrian.chosen_exit

            near_exit = pedestrian.is_near_exit()

            congestion = grid.check_congestion(pedestrian.position)

            path = get_path(congestion, near_exit, pedestrian, exit, selected_static_field, cache, grid)

            if len(path) > 1:
                p1 = pedestrian.position
                p2 = path[1]
                prefered_next_move = tuple(b - a for a, b in zip(p1, p2))

            if steps % 3 == 0 and steps != 0:
                cache.clear_cache()

            preference_matrix = PreferenceMatrix()

            # Rotaciona a matriz de preferencias baseado no proximo passo do pedestre, colocando a maior prob para o proximo passo preferido
            rotated_preference_matrix = np.array(preference_matrix.rotate_matrix(prefered_next_move))

            # Retorna uma matriz contendo os valores do dynamic_field para os vizinhos da posição atual
            dynamic_field_neighbors = dynamic_field.get_neighbors_matrix(pedestrian.position)

            # Calcula os valores da matriz de preferencias levando em conta o static e o dynamic Fields
            preference_matrix = np.exp(dynamic_field_neighbors) * np.exp(rotated_preference_matrix * 5)

            # Normaliza a matriz de preferencia para que a soma das probabilidades presentes nela nunca seja maior do que 1
            normalized_preference_matrix = mo.normalize_matrix(preference_matrix)

            # calcula os possiveis movimentos para a posição
            possible_moves = pedestrian.get_possible_moves(width, height, moves, grid)

            move_null = True
            while move_null:
                # Retorna o proximo movimento baseado na matriz de preferencias:
                chosen_next_move = pedestrian.chose_next_move(normalized_preference_matrix, possible_moves)[0]
                if chosen_next_move != None:
                    move_null = False

            pedestrian.prefered_move = chosen_next_move
            pedestrian.prefered_next_position = (p1[0] + chosen_next_move[0], p1[1] + chosen_next_move[1])

        # Resolve os conflitos
        pedestrians_info.solve_conflicts()

        # passar as posições anteriores e as futuras depois de todos os conflitos resolvidos, retornar o grid com as novas posições e se cada pedestre já atingiu a saida
        grid.grid, dynamic_field = pedestrians_info.update_pedestrians_info(dynamic_field, exits, grid.grid)

        frames.append(grid.grid.copy())
        steps += 1

    create_animation(frames)


if __name__ == "__main__":
    main()
