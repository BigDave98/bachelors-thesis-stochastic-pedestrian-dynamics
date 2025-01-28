width = 50
height = 50

num_pedestrians = 250

exits = ((30, 0),  #lateral esquerda
          (height-1, width//2),  # Saída inferior , (height-1, width//2 + 1)
          (30,49) #lateral direita
)

preference_matrix = [[0.055, 0.85, 0.055],
                     [0.01, 0, 0.01],
                     [0.007, 0.006, 0.007]]

moves = [[(-1, -1), (-1, 0), (-1, 1)],
           [(0, -1), (0,0), (0, 1)],
           [(1, -1),  (1, 0), (1, 1)]]