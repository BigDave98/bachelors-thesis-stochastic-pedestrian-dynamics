import numpy as np
import random
from utils import directions
from typing import Optional, Tuple, List, Any, Union
from numpy.typing import NDArray

class Pedestrian:
    """
        Represents a single pedestrian in a crowd movement simulation.

        This class implements the movement logic and decision making of a pedestrian
        in a discretized environment (grid), considering obstacles and exits.

        Attributes:
            id (int): Unique identifier for the pedestrian.
            position (tuple): Current position in the grid (y, x).
            best_move (tuple): Best movement calculated based on static_field.
            prefered_move (tuple): Calculated preferred movement for the next step.
            prefered_next_position (tuple): Next preferred position based on chosen movement.
            chosen_exit (tuple): Coordinates of the chosen exit destination (y, x).
        """
    def __init__(self) -> None:
        """Initialize a new pedestrian with default values."""
        self.id: int = 0
        self.position: Optional[Tuple[int, int]] = None
        self.best_move: Optional[Tuple[int, int]] = None
        self.prefered_move: Optional[Tuple[int, int]] = None
        self.prefered_next_position: Optional[Tuple[int, int]] = None
        self.prob_prefered_next_position: Optional[int] = None
        self.chosen_exit: Optional[Tuple[int, int]] = None


    def is_near_exit(self, radius=3)  -> bool:
        """
        Check if the pedestrian is near their chosen exit.

        Args:
            radius (int, optional): Proximity radius in cells. Defaults to 3.

        Returns:
            bool: True if pedestrian is within exit radius, False otherwise.
        """
        y, x = self.position
        exit_y, exit_x = self.chosen_exit

        return abs(y - exit_y) <= radius and abs(x - exit_x) <= radius

    def is_in_room(self, rooms_info: List[dict]) -> Tuple[bool, Optional[Tuple[int, int]]]:
        """
        Check if the pedestrian is inside a room and return the door position.

        Args:
            rooms_info (list): List of dictionaries containing room information.
                        Each dictionary must contain room coordinates('start', 'end') and 'door' keys.

        Returns:
            tuple: Pair (is_in_room, door_position) where:
                - is_in_room (bool): True if in a room, False otherwise
                - door_position (tuple or None): Door position if in a room,
                None otherwise
                """
        y, x = self.position

        for room in rooms_info:
            start_y, start_x = room['start']
            end_y, end_x = room['end']

            # Check if pedestrian is at the door
            if self.position == room['door']:
                return False, None

            # Check is pedestrian is inside the room
            if start_y <= y < end_y and start_x <= x < end_x:
                return True, room['door']

        return False, None

    def get_neighbors(self, grid: Any) -> List[Tuple[int, int]]:
        """
        Get valid neighboring cells for movement.

        Args:
            grid (Grid): Grid object containing environment information.

        Returns:
            list: List of tuples (y, x) representing valid neighboring cells.

        Note:
            Cells with value 3 in the grid are considered walls and are ignored.
        """
        rows, cols = grid.height, grid.width
        neighbors = []

        for dy, dx in directions:
            new_y, new_x = self[0] + dy, self[1] + dx
            if (0 <= new_y < rows and 0 <= new_x < cols and grid[new_y, new_x] != 3):  # Verifica se não é parede
                neighbors.append((new_y, new_x))

        return neighbors

    def get_possible_moves(
        self,
        width: int,
        height: int,
        moves: List[List[Tuple[int, int]]],
        grid: NDArray,
        center_x: int = 1,
        center_y: int = 1
    ) -> NDArray:
        """
        Calculate all possible moves considering the environment.

        Args:
            width (int): Grid width.
            height (int): Grid height.
            moves (list): List of possible moves.
            grid (numpy.ndarray): Matrix representing the environment.
            center_x (int, optional): Center x coordinate. Defaults to 1.
            center_y (int, optional): Center y coordinate. Defaults to 1.

        Returns:
            numpy.ndarray: 3x3 matrix containing possible moves or None for invalid moves.
        """
        possible_moves = np.zeros((3, 3), dtype=object)
        cell_position = list(self.position)

        for line in moves:
            for move in line:
                new_pos =  tuple(a + b for a, b in zip(cell_position, move))
                pos_x = center_x + move[0]
                pos_y = center_y + move[1]

                # Verifica se o movimento é válido (dentro do grid e não é parede)
                if ((0 <= new_pos[0] < height and 0 <= new_pos[1] < width and grid[new_pos[0], new_pos[1]] != 3 and grid[new_pos[0], new_pos[1]] != 1) or move == ( 0,  0)):
                    possible_moves[pos_x, pos_y] = move

                else:
                    possible_moves[pos_x, pos_y] = None

        return possible_moves

    def get_best_move(self, path: List[Tuple[int, int]]) -> None:
        """
        Determine the best move based on the provided path.

        Args:
            path (list): List of positions representing the path to the goal.
        """
        if len(path) > 1:
            p1 = self.position
            p2 = path[1]

            self.best_move = tuple(b - a for a, b in zip(p1, p2))

    def chose_next_move(self,
            rotated_preference_matrix: NDArray,
            moves: List[List[Optional[Tuple[int, int]]]]
    ) -> List[Optional[Tuple[int, int]]]:
        """
        Choose next move based on a preference matrix.

        Args:
            rotated_preference_matrix (numpy.ndarray): Rotated preference matrix.
            moves (list): List of possible moves.

        Returns:
            tuple: Chosen move based on preference matrix probabilities.
        """
        moves_ = []
        for line in moves:
            for move in line:
                moves_.append(move)

        probs = np.array(rotated_preference_matrix).flatten()
        self.prefered_move = random.choices(moves_, probs)[0]

        next_move_index = moves_.index(self.prefered_move)
        self.prob_prefered_next_position = probs[next_move_index]

    def get_move(
        self,
        matrix: NDArray,
        possible_moves: NDArray
    ) -> None:
        """
        Get a valid move based on the preference matrix.

        Args:
            matrix (numpy.ndarray): Preference matrix.
            possible_moves (numpy.ndarray): Matrix of possible moves.

        Note:
            Keeps trying until a valid (non-None) move is found.
        """
        move_null = True
        while move_null:
            # Return next move based on the preference matrix
            self.chose_next_move(matrix, possible_moves)

            if self.prefered_move != None:
                move_null = False





