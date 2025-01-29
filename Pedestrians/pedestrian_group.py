import random
from .pedestrian import Pedestrian
from collections import Counter
from typing import List, Tuple, Any
from numpy.typing import NDArray


class Pedestrians:
    """
       Manages a collection of pedestrians and handles their movement conflicts.

       This class is responsible for managing multiple pedestrians, resolving conflicts
       when multiple pedestrians want to move to the same position, and updating their
       positions on the grid.

       Attributes:
           info (List[Pedestrian]): List of pedestrian objects.
           positions (List[Tuple[int, int]]): Current positions of all pedestrians.
           prefered_next_positions (List[Tuple[int, int]]): Desired next positions
               of all pedestrians.
       """
    def __init__(self):
        """Initialize an empty pedestrians collection."""
        self.info: List[Pedestrian] = []
        self.positions: List[Tuple[int, int]] = []
        self.prefered_next_positions: List[Tuple[int, int]] = []

    def solve_conflicts(self) -> None:
        """
        Resolve conflicts when multiple pedestrians want to move to the same position.

        This method implements a conflict resolution strategy where, when multiple
        pedestrians want to move to the same position, one is randomly chosen to
        move while others stay in their current positions.
        """
        conflict = True
        while conflict:
            # Update current positions and preferred next positions
            self.positions = [pedestrian.position for pedestrian in self.info]
            self.prefered_next_positions = [pedestrian.prefered_next_position for pedestrian in self.info]

            counter = Counter(self.prefered_next_positions)

            # Check if there are any conflicts (same position desired by multiple pedestrians)
            if sum(counter.values()) != len(set(self.prefered_next_positions)):
                # Get positions with conflicts (more than one pedestrian wants to move there)
                conflicts = [item for item, count in counter.items() if count > 1]

                # Map conflicting positions to indices of pedestrians wanting to move there
                conflicts_index = {position: [idx for idx, pos in enumerate(self.prefered_next_positions) if pos == position]
                                   for position in conflicts}  # indices

                # Randomly select one pedestrian for each conflicting position
                random_pedestrian = {
                    position: [random.choices(value)[0] for key, value in conflicts_index.items() if key == position]
                    for position in conflicts_index}  # w

                # Resolve conflicts by making non-selected pedestrians stay in place
                for key in conflicts_index:
                    conflicts_index[key].remove(random_pedestrian[key][0])
                    for conflict_index in conflicts_index[key]:
                        self.info[conflict_index].prefered_next_position = self.info[conflict_index].position

                self.prefered_next_positions = [pedestrian.prefered_next_position for pedestrian in self.info]
            else:
                conflict = False


    #Função deve ser definida para a classe grid e não pedestre
    def update_pedestrians_info(
        self,
        dynamic_field: Any,  # Type Any used as DynamicField class isn't imported
        exits: List[Tuple[int, int]],
        grid: NDArray
    ) -> Tuple[NDArray, Any]:
        """
        Update pedestrians' positions, the grid and dynamic field state.

        Args:
            dynamic_field: Dynamic field object that influences pedestrians flow.
            exits: List of exit positions on the grid.
            grid: Current state of the simulation grid.

        Returns:
            Tuple containing:
                - Updated grid
                - Updated dynamic field
        """
        # Clear old positions on grid
        grid[tuple(zip(*[p.position for p in self.info]))] = 0

        # Get positions that need dynamic field update
        positions_update_dynamic_field = [pedestrian.position for pedestrian in self.info
                                          if pedestrian.position != pedestrian.prefered_next_position]

        dynamic_field.update_dynamic_field(positions_update_dynamic_field)

        # Remove pedestrians who reached exits
        self.info = [p for p in self.info if p.prefered_next_position not in exits]

        # Update positions
        for p in self.info:
            p.position = p.prefered_next_position

        # If no pedestrians left return
        if not self.info:
            return grid, dynamic_field

        # Update grid with new positions
        new_positions = [p.position for p in self.info]
        grid[tuple(zip(*new_positions))] = 1

        return grid, dynamic_field




