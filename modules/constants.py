### Room Scenario Params ###

# Amount of subdivisions to divide a square room into.
N = 40
DX = 1 / (N-1)
# Smoothing param, lower to reduce large changes in temperature state between iterations.
OMEGA = 0.6
# Number of iterations to run.
N_ITERATIONS = 10
# Set to True to include the extension room, otherwise just computes the three-room floorplan.
INCLUDE_ROOM4 = True

### Room and Boundary Initial Temperatures ###

HEATER_TEMP = 40.0  # Heating Source
WINDOW_TEMP = 5.0   # Cooling Source
WALL_TEMP = 15.0    # Neutral Wall
FLOOR_TEMP = 0.0    # Generic starting room temperature, changes through iterations

### Animation/Plotting Params ###

# Set to true to save all iterations and animate from the initial state to the end state.
ANIMATE = True
# Set to True to crop out the boundary conditions, so they won't show in the plot.
CROP = False

# Keyword args to configure the plotting functionality, should be compatible with
# `plot_temperature()`
PLOT_PARAMS = { # Default params
    "cmap": "inferno",  # Chosen color map scheme
    "norm_min": WINDOW_TEMP,      # Normalizes 0 to be the coldest value
    "norm_max": HEATER_TEMP,     # Normalizes 40 to be the hottest value
}

# Visual change to heat spreading through water
PLOT_PARAMS_OCEAN = {
    "cmap": "ocean",
    "norm_min": -15,
    "norm_max": 50,
}

# Visual change to heat leaving water
PLOT_PARAMS_ICE = {
    "cmap": "ocean",
    "norm_min": -80,
    "norm_max": 40,
}

# Keyword args to configure the animation functionality, should be compatible with
# `matplotlib.animation.FuncAnimation()`
DEFAULT_ANIMATION_PARAMS = {
    "interval": 500,         # (ms) delay between frames
    "repeat_delay": 2000,   # (ms) delay before restarting animation
    "repeat": True,         # Set to true to loop the animation
}

ANIMATION_PARAMS = {
    "interval": 80,
    "repeat_delay": 2000,
    "repeat": True,
}
