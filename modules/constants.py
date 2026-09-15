### Room Scenario Params ###

# Amount of subdivisions to divide a square room into.
DX = 1 / 30
# Smoothing param, lower to reduce large changes in temperature state between iterations.
OMEGA = 0.8 
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
