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
        floorplan_builder = lambda x: x,
        main_title = "Heat Flow Visualized",
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

    :param room_states: A list of snapshots, each one a list of individual room states. Expecting that those room states are ordered [room_1, room_2, ...] matching the assignment diagram.
    :param floorplan_builder: A function which is expected to run on each frame of "rooms" state passed as input. For instance, if each frame of rooms state is [room_1, room_2, room_3], that array will be passed to this builder function. The builder function will then construct a single nparray to serve as the floorplan and return that to be rendered by the plotting logic. (Note: See the plot_visuals test file for example usage.)
    :param main_title: The title to display for the plot window.
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
    fig.suptitle(main_title, weight=700, size="xx-large")

    # Adjust figure to reduce excess whitespace and low vertical alignment.
    fig.subplots_adjust(
        top=0.85,     bottom=0.15,
        left=0.05,  right=0.95,
        wspace=0.1, hspace=1.
    )

    # Create a colorizer with a predefined norm to be shared across all images
    norm = mcolors.Normalize(vmin=norm_min, vmax=norm_max)
    colorizer = mcolorizer.Colorizer(norm=norm, cmap=cmap)

    # Run each frame of room_states passed as input through the builder function to construct
    # frames of floorplans for display. Naturally it is assumed that the data and function are
    # compatible.
    floorplan_frames = [floorplan_builder(rooms) for rooms in room_states]

    # Attach heatmap to each of the three displays.
    images = []
    for ax, plot_data in zip(axes.flat, setup_plot_data(floorplan_frames, show_animation)):
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

    # Finally, show plot as a maximized window
    plt.show()
