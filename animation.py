import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import Matrix.matrix_operations as mo
import numpy as np
from utils import exits, moves, width, height
from PathFinding import get_path
from matplotlib.animation import FuncAnimation
from Matrix import PreferenceMatrix

def get_frames(grid, cache, rooms, pedestrians_info, dynamic_field, static_field):
    frames = []
    steps = 0
    while pedestrians_info.info:
        pedestrians_info.prefered_next_positions, pedestrians_info.prefered_moves = [], []

        # Calcula a prob da proxima posição preferida para cada pedestre
        for pedestrian in pedestrians_info.info:
            # Verifica se esta dentro de um quarto, caso esteja retorna TRUE e a posição da porta em questão
            inside_room, door_position = pedestrian.is_in_room(rooms)

            selected_static_field, pedestrian = static_field.get_static_field(inside_room,
                                                                              door_position,
                                                                              pedestrian,
                                                                              exits,
                                                                              grid)

            path = get_path(grid.check_congestion(pedestrian.position),
                            pedestrian.is_near_exit(),
                            pedestrian,
                            pedestrian.chosen_exit,
                            selected_static_field,
                            cache,
                            grid)

            pedestrian.get_best_move(path)

            cache.clear_cache(steps)

            # Retorna uma matriz contendo os valores do dynamic_field para os vizinhos da posição atual
            dynamic_field_neighbors = dynamic_field.get_neighbors_matrix(pedestrian.position)

            preference_matrix = PreferenceMatrix()
            preference_matrix.get_matrix(pedestrian.best_move, dynamic_field_neighbors)

            # calcula os possiveis movimentos para a posição
            possible_moves = pedestrian.get_possible_moves(width, height, moves, grid)

            pedestrian.get_move(preference_matrix.matrix, possible_moves)
            pedestrian.prefered_next_position = tuple(a + b for a, b in zip(pedestrian.position, pedestrian.prefered_move))

        # Resolve os conflitos
        pedestrians_info.solve_conflicts()

        # passar as posições anteriores e as futuras depois de todos os conflitos resolvidos, retornar o grid com as novas posições e se cada pedestre já atingiu a saida
        grid.grid, dynamic_field = pedestrians_info.update_pedestrians_info(dynamic_field, exits, grid.grid)

        frames.append(grid.grid.copy())
        steps += 1

    return frames

def create_animation(frames):
    colors = ['white', 'black', 'red', 'gray']
    cmap = mcolors.ListedColormap(colors)
    norm = mcolors.BoundaryNorm(boundaries=[0, 0.5, 1.5, 2.5, 3.5], ncolors=4)

    plt.ioff()
    fig, ax = plt.subplots(figsize=(8, 8))

    def animate(frame_num):
        ax.clear()
        im = ax.imshow(frames[frame_num], cmap=cmap, norm=norm)
        ax.set_title(f'Step {frame_num}')
        ax.set_xlim(-1, len(frames[0][0]))  # Define limites do eixo x
        ax.set_ylim(-1, len(frames[0]))     # Define limites do eixo y
        return [im]

    anim = FuncAnimation(fig, animate,
                        frames=len(frames),
                        interval=200,
                        repeat=True)

    plt.ion()
    plt.show(block=True)




