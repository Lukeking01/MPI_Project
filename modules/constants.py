### Room Scenario Params ###

# Amount of subdivisions to divide a square room into.
DX = 1 / 30
# Smoothing param, lower to reduce large changes in temperature state between iterations.
OMEGA = 0.8 
# Number of iterations to run.
N_ITERATIONS = 10
# Set to True to include the extension room, otherwise just computes the three-room floorplan.
INCLUDE_ROOM4 = False

### Animation/Plotting Params ###

# Set to true to save all iterations and animate from the initial state to the end state.
ANIMATE = False
# Set to True to crop out the boundary conditions, so they won't show in the plot.
CROP = True
