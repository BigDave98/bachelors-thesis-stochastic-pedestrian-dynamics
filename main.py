from config import *
from Fields import FloorField, DynamicField, StaticField
from Cache import Cache
from Pedestrians import Pedestrians
from animation import create_animation, get_frames
def main():
    steps = 0
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

    frames = get_frames(grid, cache, rooms, pedestrians_info, dynamic_field, static_field)

    create_animation(frames)


if __name__ == "__main__":
    main()

