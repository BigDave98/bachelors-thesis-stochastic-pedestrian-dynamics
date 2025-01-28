width = 50
height = 50

num_pedestrians = 10

exits = ((30, 0),  #left wall
          (height-1, width//2),  # Top exit
          (30,49) #right wall
)

preference_matrix = [[0.055, 0.85, 0.055],
                     [0.01, 0, 0.01],
                     [0.007, 0.006, 0.007]]

moves = [[(-1, -1), (-1, 0), (-1, 1)],
           [(0, -1), (0,0), (0, 1)],
           [(1, -1),  (1, 0), (1, 1)]]

directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # ortogonais
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # diagonais
        ]


def get_min_max(position, grid, radius):
    y, x = position
    y_min = max(0, y - radius)
    y_max = min(grid.shape[0], y + radius + 1)
    x_min = max(0, x - radius)
    x_max = min(grid.shape[1], x + radius + 1)

    return y_min, y_max, x_min, x_max