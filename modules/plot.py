import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colorizer as mcolorizer
import matplotlib.colors as mcolors
import matplotlib.animation as animation

def create_dummy_array(n: int):
    """
    Dummy function, simply creates a mock output of an n x n grid, with random temperature
    data in cells ranging from 20 to 80.
    """
    return 20 + 80 * np.random.random((n, n))

def cleanup_ax(ax):
    """
    Cleans up the axes by removing tick marks.
    """
    ax.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom = False, labelleft = False)

def setup_plot_data(room_states):
    """
    Collects the plot data with useful info describing what should be visualized and customizing how.
    It is hard-coded behavior in this function that the output array will be:
    
    - The initial room state.
    - An animation from the initial to final room states.
    - The final room state.

    Note: "data" will be a single room state frame, unless it's meant to be animated, in which case "data"
    should be an array of frames to animate between.
    """
    return [
        {
            "data": room_states[0],
            "title": "Initial State",
            "animate": False,
        },
        {
            "data": room_states,
            "title": "Animation",
            "animate": True,
        },
        {
            "data": room_states[-1],
            "title": "Final State",
            "animate": False,
        },
    ]

def plot_temperature(room_states):
    """
    Accepts an array of room state snapshots, and renders them in a series of heatmaps. 
    Namely, the initial room state, an animation switching between room states, and a final
    room state.

    # TODO: Determine how to stitch together three separate rooms into a single graph object.
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

    # Configure subplots
    fig, axes = plt.subplots(1, 3)
    fig.suptitle("Heat Flow Visualized")

    # Create a colorizer with a predefined norm to be shared across all images
    norm = mcolors.Normalize(vmin=0, vmax=100)
    cmap = "inferno"
    colorizer = mcolorizer.Colorizer(norm=norm, cmap=cmap)

    # Attach heatmap to each of the three displays.
    images = []
    for ax, plot_data in zip(axes.flat, setup_plot_data(room_states)):
        # Update subplot title
        ax.set_title(plot_data["title"])
        # Clean subplot details
        cleanup_ax(ax)

        if not plot_data["animate"]:
            # Draw heatmap
            images.append(ax.imshow(plot_data["data"], colorizer=colorizer))
        else:
            # Animate heatmap frames
            anim_img = ax.imshow(plot_data["data"][0], colorizer=colorizer)

            # Updates the frame rendered in the axes image with the incoming frame from the Animation object.
            def update(frame_data):
                anim_img.set_array(frame_data)
                return [anim_img] 

            anim = animation.FuncAnimation(
                fig,
                update,
                frames=plot_data["data"],
                interval=700, # Delay in (ms)
                repeat=True,
                repeat_delay=2000,
                # blit=False, # Set to true if more efficient rendering is desired, but note that an
                              # init_func may be required to draw the first frame to a non-white background.
            )
            images.append(anim)

    # Display shared colorbar
    fig.colorbar(images[0], ax=axes, orientation='horizontal', fraction=0.1)

    plt.show()

dummy_data = [create_dummy_array(n) for n in [50, 30, 20, 15, 12, 10]]

plot_temperature(dummy_data)
