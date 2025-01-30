from typing import List, Tuple, Dict, Any, Optional
import random
from PathFinding import *
import numpy as np
from numpy.typing import NDArray

Position = Tuple[int, int]
StaticFieldType = Dict[str, Any]

class StaticField:
    """
    Manages static fields for pedestrian pathfinding.

    This class handles the calculation and selection of static fields that guide
    pedestrians towards exits through the environment.

    Attributes:
        width (int): Width of the environment grid
        height (int): Height of the environment grid
        static_field (NDArray): Matrix storing static field values
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize static field with given dimensions.

        Args:
            width: Width of the environment grid
            height: Height of the environment grid
        """
        self.width = width
        self.height = height

        self.static_field = np.zeros((width, height), dtype=object)

    def __getitem__(self, position: Position) -> Any:
        """
        Enable grid access using grid[y,x] syntax.

        Args:
            position: Tuple of (x, y) coordinates

        Returns:
            Value at the specified position
        """
        x, y = position
        return self.static_field[x, y]

    def __setitem__(self, position: Position, value: Any) -> None:
        """
        Enable grid modification using grid[y,x] = value syntax.

        Args:
            position: Tuple of (x, y) coordinates
            value: Value to set at the position
        """
        x, y = position
        self.static_field[x, y] = value

    def set_static_field_ij(self, grid: NDArray, position: Position, exits: List[Position]) -> None:
        """
        Calculate static field values for a given position to all exits.

        Args:
            grid: Environment grid
            position: Current position to calculate fields from
            exits: List of exit positions

        Note:
            Only calculates if the position hasn't been calculated before
        """
        if self.static_field[position] == 0:
            static_fields_ij = []

            # Return steps, positions and number of steps to desired exit
            for exit in exits:
                static_field_ij = find_shortest_path(grid, exit, position)
                static_fields_ij.append(static_field_ij)

            self.static_field[position] = static_fields_ij

    def prob_field_Sij(self, position: Position, len_exits: int) -> List[float]:
        """
        Calculate probabilities for each static field at a position.

        Args:
            position: Position to calculate probabilities for
            len_exits: Number of exits

        Returns:
            List of normalized probabilities for each static field
        """
        possible_steps_to_exit = list(map(lambda x: x['steps'], self.static_field[position]))
        sum_static_field_ij = sum(possible_steps_to_exit)

        probsSx = []
        probsSx_ = []

        # Probability of cell at position (ij) having Sij(wp) as its SF
        for i in range(len_exits):
            probSx = (1 / self.static_field[position][i]['steps'] / (1 / sum_static_field_ij))  # Função 3 do artigo
            probsSx.append(probSx)

        sum_probs = sum(probsSx)

        for i in probsSx:
            probSx_ = i / sum_probs
            probsSx_.append(probSx_)

        return list(probsSx_)

    def select_static_field(
            self,
            position: Position,
            prob_field_sij: List[float]
    ) -> List[StaticFieldType]:
        """
        Select a static field based on calculated probabilities.

        Args:
            position: Current position
            prob_field_sij: List of probabilities for each field

        Returns:
            Selected static field based on probabilities
        """
        return random.choices(self.static_field[position], prob_field_sij)

    def get_static_field(
            self,
            inside_room: bool,
            door_position: Optional[Position],
            pedestrian: Any,
            exits: List[Position],
            grid: NDArray
    ) -> Tuple[StaticFieldType, Any]:
        """
        Get appropriate static field for a pedestrian based on their situation.

        Args:
            inside_room: Whether the pedestrian is inside a room
            door_position: Position of the door if in a room
            pedestrian: Pedestrian object
            exits: List of available exits
            grid: Environment grid

        Returns:
            Tuple containing:
                - Selected static field
                - Updated pedestrian object

        Note:
            Updates pedestrian's chosen exit if necessary
        """
        if inside_room:
            self.set_static_field_ij(grid, pedestrian.position, [door_position])

            if pedestrian.chosen_exit == None:
                selected_static_field = self.static_field[pedestrian.position][0]
                pedestrian.chosen_exit = selected_static_field['exit']
            else:
                selected_static_field = self.static_field[pedestrian.position][0]
        else:
            # Assign static field values based on current pedestrian position
            self.set_static_field_ij(grid, pedestrian.position, exits)

            # Calculate probability for each static field based on distance to exit
            prob = self.prob_field_Sij(pedestrian.position, len(exits))

            if pedestrian.chosen_exit == None or (pedestrian.chosen_exit not in exits and not inside_room):

                # Select static field based on probabilities
                selected_static_field = self.select_static_field(pedestrian.position, prob)[0]
                pedestrian.chosen_exit = selected_static_field['exit']

            else:
                selected_static_field = [field for field in self.static_field[pedestrian.position] if field['exit'] == pedestrian.chosen_exit][0]

        return selected_static_field, pedestrian


