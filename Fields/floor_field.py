from typing import List, Tuple, Dict, Union
import numpy as np
import random
from Pedestrians import Pedestrian
from utils import get_min_max
from numpy.typing import NDArray

Position = Tuple[int, int]
Size = Tuple[int, int]
RoomInfo = Dict[str, Union[Position, Position]]


class FloorField:
    """
    Manages the floor environment grid for pedestrian simulation.

    This class handles the creation and management of the environment grid,
    including walls, exits, rooms, and pedestrian positioning.

    Attributes:
        width (int): Width of the environment grid
        height (int): Height of the environment grid
        grid (NDArray): Matrix representing the environment where:
            0: Empty cell
            1: Occupied by pedestrian
            2: Exit
            3: Wall
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize floor field with given dimensions.

        Args:
            width: Width of the environment grid
            height: Height of the environment grid
        """
        self.width = width
        self.height = height
        self.grid: NDArray = np.zeros((width, height))

    def __getitem__(self, position: Position) -> float:
        """
        Enable grid access using grid[y,x] syntax.

        Args:
            position: Tuple of (y, x) coordinates

        Returns:
            Value at the specified position
        """
        return self.grid[position]

    def __setitem__(self, position: Position, value: float) -> None:
        """
        Enable grid modification using grid[y,x] = value syntax.

        Args:
            position: Tuple of (y, x) coordinates
            value: Value to set at the position
        """
        self.grid[position] = value

    def add_exit(self, exits: List[Position]) -> None:
        """
        Add exits to the environment grid.

        Args:
            exits: List of exit coordinates
        """
        for exit_coordinates in exits:
            self.grid[exit_coordinates] = 2

    def add_walls(self, start_pos: Position, size: Size, door_pos: Position) -> None:
        """
        Add walls to create a room with a door.

        Args:
            start_pos: Starting position (y, x) of the room
            size: Room dimensions (height, width)
            door_pos: Door position (y, x)
        """
        y, x = start_pos
        h, w = size

        # Add walls
        self.grid[y:y + h, x] = 3  # Left wall
        self.grid[y:y + h, x + w - 1] = 3  # Right wall
        self.grid[y, x:x + w] = 3  # Top wall
        self.grid[y + h - 1, x:x + w] = 3  # Bottom wall

        # Add door
        door_y, door_x = door_pos
        self.grid[door_y, door_x] = 0

    def setup_rooms(self) -> List[RoomInfo]:
        """
        Create 3 rooms at specified positions.

        Returns:
            List of dictionaries containing room information:
                - 'start': Starting position (y, x)
                - 'end': End position (y, x)
                - 'door': Door position (y, x)
        """
        rooms_info: List[RoomInfo] = []

        # Room 1: Bottom Left
        room1_start = (self.height - 15, 5)
        room1_size = (15, 15)
        door1_pos = (self.height - 15, 12)
        self.add_walls(room1_start, room1_size, door1_pos)

        rooms_info.append({
            'start': room1_start,
            'end': (room1_start[0] + room1_size[0], room1_start[1] + room1_size[1]),
            'door': door1_pos
        })

        # Room 2: Bottom Right
        room2_start = (self.height - 15, 30)
        room2_size = (15, 20)
        door2_pos = (self.height - 15, 40)
        self.add_walls(room2_start, room2_size, door2_pos)

        rooms_info.append({
            'start': room2_start,
            'end': (room2_start[0] + room2_size[0], room2_start[1] + room2_size[1]),
            'door': door2_pos
        })

        # Room 3: Top Center
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

    def available_positions(self, num_pedestrians: int) -> List[Position]:
        """
        Find available positions for pedestrian placement.

        Args:
            num_pedestrians: Number of pedestrians to place

        Returns:
            List of available positions (y, x)
        """
        # Find coordinates that are free (value 0) in the grid
        available_positions = [(i, j) for i in range(self.height) for j in range(self.width) if self.grid[i, j] == 0]

        return available_positions

    def set_pedestrians(self, pedestrians: any, num_pedestrians: int) -> List[Pedestrian]:
        """
        Place pedestrians randomly in available positions.

        Args:
            pedestrians: Pedestrians collection object
            num_pedestrians: Number of pedestrians to place

        Returns:
            List of placed pedestrian objects
        """
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

    def check_congestion(
            self,
            position: Position,
            threshold: int = 3,
            radius: int = 2
    ) -> bool:
        """
        Check if there is congestion around a position.

        Args:
            position: Current position (y, x)
            threshold: Number of occupied cells to consider congestion
            radius: Radius to check neighborhood

        Returns:
            True if number of occupied cells > threshold
        """
        y_min, y_max, x_min, x_max = get_min_max(position, self.grid, radius)

        # Count occupied cells (value 1) in neighborhood
        occupied_cells = np.sum(self.grid[y_min:y_max, x_min:x_max] == 1)

        return bool(occupied_cells > threshold)


