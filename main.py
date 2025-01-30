from typing import List, Dict, Any
from utils import width, height, exits, num_pedestrians
from Fields import FloorField, DynamicField, StaticField
from Cache import Cache
from Pedestrians import Pedestrians
from animation import create_animation, get_frames

def main() -> None:
    """
    Main simulation function for pedestrian evacuation.

    This function sets up and runs the pedestrian evacuation simulation by:
    1. Initializing the caching system
    2. Creating and configuring the environment grid
    3. Setting up pedestrian positions
    4. Creating dynamic and static fields
    5. Running the simulation
    6. Displaying the animation
    """
    # Initialize path caching system
    cache = Cache()

    # Create and configure environment grid with exits and rooms
    grid = FloorField(width, height)
    grid.add_exit(exits)
    rooms = grid.setup_rooms()

    # Initialize and positionate pedestrians
    pedestrians_info = Pedestrians()
    pedestrians_info.info = grid.set_pedestrians(pedestrians_info, num_pedestrians)

    # Initialize dynamic and static fields
    dynamic_field, static_field = DynamicField(width, height), StaticField(width, height)

    # Run simulation and create animation
    frames = get_frames(grid, cache, rooms, pedestrians_info, dynamic_field, static_field)
    create_animation(frames)


if __name__ == "__main__":
    main()

