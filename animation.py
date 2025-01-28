import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors


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




