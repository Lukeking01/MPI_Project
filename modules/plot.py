import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colorizer as mcolorizer
import matplotlib.colors as mcolors
import matplotlib.animation as animation

def cleanup_ax(ax):
    """
    Cleans up the axes by removing tick marks, and removing the borders.

    :param ax: Axes instance defining matplotlib subplots.
    :returns None:
    """
    ax.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom = False, labelleft = False)
    ax.axis('off')


def setup_plot_data(room_states, show_animation = False):
    """
    Collects the plot data with useful info describing what should be visualized and customizing how.
    If show_animation is set to true, the first plot will be an animation through all room states.
    Otherwise it will just be a static heatmap showing the initial room state.

    Note, "data" will be a single room state frame, unless it's meant to be animated, in which case "data"
    should be a list of frames to animate between.

    :param room_states: List of frames defining the room state.
    :param show_animation: Set to True to configure the first plot to show a full animation. Set to False
    to just show the static initial frame.
    :returns list[dict]: A list of dictionaries defining details used to build a subplot.
    """

    plots = []
    if show_animation:
        # Define plot information with animation.
        plots.append({
            "data": room_states,
            "title": "Animation",
            "animate": True,
        })
    else:
        # Define plot information with static starting state.
        plots.append({
            "data": room_states[0],
            "title": "Initial State",
            "animate": False,
        })
    # Final room state is always the second plot.
    plots.append({
        "data": room_states[-1],
        "title": "Final State",
        "animate": False,
    })
    return plots


def plot_temperature(
        room_states,
        show_animation = False,
        norm_min = 0,
        norm_max = 40,
        cmap = "inferno",
    ):
    """
    Accepts a list of room state snapshots, and renders them in a series of heatmaps. 

    The first heatmap will either show the static initial frame, or an animation through
    the frames, pausing at the end. The second heatmap will always show the final state,
    the result after "n" iterations.

    :param room_states: A list of snapshots, each one a list of individual room states. Expecting that those room states are ordered \[room_1, room_2, ...\] matching the assignment diagram.
    :param show_animation: Set to True to show an animation through all room states in the left plot. Otherwise will display the heatmap of the initial frame.
    :param norm_min: Minimum expected value to set to the "coolest" color.
    :param norm_max: Maximum expected value to set to the "hottest" color.
    :param cmap: Custom cmap color set to use in the visualization. Some available ones that look nice are: "inferno", "viridis", "magma", "plasma", "cividis", "ocean".
    
    :returns None:

    ---

    TODO: Room states will be sent to this method in the form of a list of rooms. So "room_states"
            will be a list of a list of individual room states, we need to convert that to a list
            of glued room states before sending that data through to setup_plot_data().
    TODO: Certain theming and timing vars should be moved to parameters with reasonable defaults.
    """

    # Setup subplots.
    fig, axes = plt.subplots(1, 2, constrained_layout=False)
    fig.suptitle("Heat Flow Visualized", weight=700, size="xx-large")

    # Adjust figure to reduce excess whitespace and low vertical alignment.
    fig.subplots_adjust(
        top=0.85,     bottom=0.15,
        left=0.05,  right=0.95,
        wspace=0.1, hspace=1.
    )

    # Create a colorizer with a predefined norm to be shared across all images
    norm = mcolors.Normalize(vmin=norm_min, vmax=norm_max)
    colorizer = mcolorizer.Colorizer(norm=norm, cmap=cmap)

    # Attach heatmap to each of the three displays.
    images = []
    for ax, plot_data in zip(axes.flat, setup_plot_data(room_states, show_animation)):
        # Update subplot title
        ax.set_title(plot_data["title"], size="x-large")
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
    fig.colorbar(images[1], ax=axes, orientation='horizontal', fraction=0.05)

    plt.show()


##########################################################################################

# TODO Remove once main.py connects to this file properly!
# LOCAL TESTING FOR PLOTTING FUNCTIONS

def create_dummy_array(m: int, n: int = None):
    """
    Dummy function, simply creates a mock output of an m x n grid, with random temperature
    data in cells ranging from 20 to 80.
    """
    if not n:
        n = m
    
    return 15 + 20 * np.random.random((m, n))

# --- Simple dummy example ---
dummy_data = [create_dummy_array(n) for n in [50, 30, 20, 15, 12, 10]]

# --- More fluid room layout example ---
# TODO Needs a better stacking alg I reckon...
n = 10
empty_space = np.full((n, n), fill_value=np.nan)
room_1 = np.random.normal(loc=18, scale=1.5, size=(10, 10))  # Cool room (~18°C)
room_2 = np.random.normal(loc=26, scale=1.0, size=(20, 10))  # Warm room (~22°C)
room_3 = np.random.normal(loc=33, scale=2.0, size=(10, 10))  # Hot room (~26°C)
floorplan = [np.hstack([
    np.block([[empty_space], [room_1]]),
    room_2,
    np.block([[room_3], [empty_space]])
])]

# --- Choose dummy test plot data ---
plot_temperature(dummy_data, True) # Shows animation
# plot_temperature(floorplan, True, cmap="ocean") # Shows floor layout stitching

##########################################################################################
