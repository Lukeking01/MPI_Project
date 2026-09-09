import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colorizer as mcolorizer
import matplotlib.colors as mcolors

def create_dummy_array(n: int):
    """
    Dummy function, simply creates a mock output of an n x n grid, with random temperature
    data in cells ranging from 0 to 100.
    """
    return 100 * np.random.random((n, n))

def plot_temperature(room_states):
    """
    Accepts an array of room state snapshots, and renders them in a series of heatmaps. 
    Namely, the initial room state, an animation switching between room states, and a final
    room state.

    # TODO: Certain theming and timing vars should be moved to parameters with reasonable defaults.
    # TODO: It should maybe be possible to opt in/out to the animation, since that looping forever could
            be distracting when trying to talk through the output. Or, the speed of the animation could be
            customizable.
    # TODO: Determine the best way to handle normalizing the room states data. Is it better to clamp between
            the minimum and maximum values between all iteration room states, which may have different min/max
            values between iterations. Or should some arbitrary min/max be chosen, which runs the risk of either
            not capturing the correct range, or keeping a large portion of the heatmap colors as unreachable.
            For now doing the latter since it's easier.
    """

    init_room_state = room_states[0]
    final_room_state = room_states[-1]

    # Configure subplots
    fig, axs = plt.subplots(1, 3)
    fig.suptitle("Multiple Images")
    # im = ax.imshow(create_dummy_array(), cmap="BlRe")

    # Create a colorizer with a predefined norm to be shared across all images
    norm = mcolors.Normalize(vmin=0, vmax=100)
    cmap = "inferno"
    colorizer = mcolorizer.Colorizer(norm=norm, cmap=cmap)

    # Attach heatmap to each of the three displays.
    images = []
    for ax, data in zip(axs.flat, [init_room_state, room_states[0], final_room_state]):
        images.append(ax.imshow(data, colorizer=colorizer))

    # Display shared colorbar
    fig.colorbar(images[0], ax=axs, orientation='horizontal', fraction=.1)

    plt.show()

dummy_data = [create_dummy_array(n) for n in [50, 30, 20, 15, 12, 10]]

plot_temperature(dummy_data)
