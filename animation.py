from typing import List, Tuple, Any
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from utils import exits, moves, width, height
from PathFinding import get_path
from matplotlib.animation import FuncAnimation
from Matrix import PreferenceMatrix
from numpy.typing import NDArray

Frames = List[NDArray]
Grid = NDArray
def get_frames(
   grid: Any,
   cache: Any,
   rooms: List[dict],
   pedestrians_info: Any,
   dynamic_field: Any,
   static_field: Any
) -> Frames:
    """
    Generate animation frames by simulating pedestrian movement.

   Args:
       grid: Environment grid
       cache: Path cache object
       rooms: List of room information
       pedestrians_info: Pedestrian collection object
       dynamic_field: Dynamic field object
       static_field: Static field object

   Returns:
       List of grid states representing animation frames
    """
    frames = []
    steps = 0
    while pedestrians_info.info:
        pedestrians_info.prefered_next_positions, pedestrians_info.prefered_moves = [], []

        # Calculate preferred next position for each pedestrian
        for pedestrian in pedestrians_info.info:
            # Check if inside a room, returns TRUE and door position if so
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

            # Get dynamic field values for neighbors of current position
            dynamic_field_neighbors = dynamic_field.get_neighbors_matrix(pedestrian.position)

            preference_matrix = PreferenceMatrix()
            preference_matrix.get_matrix(pedestrian.best_move, dynamic_field_neighbors)

            # Calculate possible moves for the position
            possible_moves = pedestrian.get_possible_moves(width, height, moves, grid)

            pedestrian.get_move(preference_matrix.matrix, possible_moves)
            pedestrian.prefered_next_position = tuple(a + b for a, b in zip(pedestrian.position, pedestrian.prefered_move))

        # Resolve movement conflicts
        pedestrians_info.solve_conflicts()

        # Update grid with new positions after conflicts are resolved
        grid.grid, dynamic_field = pedestrians_info.update_pedestrians_info(dynamic_field, exits, grid.grid)

        frames.append(grid.grid.copy())
        steps += 1

    return frames

def create_animation(frames: Frames) -> None:
    """
    Create and display animation of pedestrian movement.

    Args:
        frames: List of grid states representing animation frames

    Note:
        Color mapping:
            - White: Empty cell (0)
            - Black: Pedestrian (1)
            - Red: Exit (2)
            - Gray: Wall (3)
    """
    colors = ['white', 'black', 'red', 'gray']
    cmap = mcolors.ListedColormap(colors)
    norm = mcolors.BoundaryNorm(boundaries=[0, 0.5, 1.5, 2.5, 3.5], ncolors=4)

    fig, ax = plt.subplots(figsize=(8, 8))

    def animate(frame_num: int):
        """
        Update function for animation.

        Args:
            frame_num: Current frame number

        Returns:
            List containing the updated image
        """
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




