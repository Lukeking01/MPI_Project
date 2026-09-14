# Heat Simulation with OpenMPI - Course NUMN21

In this project we aim to model the temperature distribution in an apartment by
solving the heat equation. To speed up execution of this process, we use OpenMPI
to divide the initial floorplan into multiple rooms which can be solved simultaneously.

## Usage

To run the main file, you must have OpenMPI installed, and run the following:

```
mpiexec -n 3 python main.py
```

This runs main.py using mpiexec which should spin up three threads to handle
the computation. After a short delay, you should see a plot visualizing an
animation through the iterations of the program, and the final state it ended on.

Several aspects related to the plotting can be configured in main.py, for instance
the cmap can be changed to change the color mapping in the heatmaps, and the
animation can be toggled On/Off.

## Assignment Tasks

1. **Task 1:** Dirichlet-Neumann matrices when mesh width dx = 1 / 3
   
### A matrices:

#### room 1
   
          [[-4.  1.  1.  0.]
             [ 1. -3.  0.  1.]
             [ 1.  0. -4.  1.]
             [ 0.  1.  1. -3.]]

 #### room 2

       [[-4.  1.  1.  0.  0.  0.  0.  0.  0.  0.]
         [ 1. -4.  0.  1.  0.  0.  0.  0.  0.  0.]
         [ 1.  0. -4.  1.  1.  0.  0.  0.  0.  0.]
         [ 0.  1.  1. -4.  0.  1.  0.  0.  0.  0.]
         [ 0.  0.  1.  0. -4.  1.  1.  0.  0.  0.]
         [ 0.  0.  0.  1.  1. -4.  0.  1.  0.  0.]
         [ 0.  0.  0.  0.  1.  0. -4.  1.  1.  0.]
         [ 0.  0.  0.  0.  0.  1.  1. -4.  0.  1.]
         [ 0.  0.  0.  0.  0.  0.  1.  0. -4.  1.]
         [ 0.  0.  0.  0.  0.  0.  0.  1.  1. -4.]]

 #### room 3
   
       [[-3.  1.  1.  0.]
         [ 1. -4.  0.  1.]
         [ 1.  0. -3.  1.]
         [ 0.  1.  1. -4.]]
### b matrices:

  #### room 1
    
            [-55.         -16.66666667 -55.         -16.66666667]
#### room 2

            [-55. -40. -15.   0. -15. -15.   0. -15.  -5. -20.]
#### room 3 

            [-17.77777778 -55.         -13.33333333 -55.        ]

### Solved matrices:

 #### room 1
 
         [[40.         15.         15.         15.        ]
         [40.         25.02126925 20.04638878 20.03080229]
         [40.         25.03868821 20.13348358 20.44885733]
         [40.         15.         15.         15.        ]]

#### room 2

        [[15.         40.         40.         15.        ]
         [15.         25.29881236 26.6707221  20.56578179]
         [15.         19.52452735 20.81829426 20.09303321]
         [15.         16.98100279 16.98489437 15.        ]
         [20.03080316 16.41458944 15.14028044 15.        ]
         [20.44885807 13.50627137 12.16163795 15.        ]
         [15.          5.          5.         15.        ]]

#### room 3 

        [[15.         15.         15.         40.        ]
         [20.56578179 19.42146932 24.81841236 40.        ]
         [20.09303328 19.59030807 24.85218011 40.        ]
         [15.         15.         15.         15.        ]]

3. **Task 2:** Is heating in the flat adequate?

The heating looks fairly adequate. The temperature settles at approximately 20 degrees in the flat (very liveable). 

3. **Task 3:** Plotted temperature distribution

    > Plot with a mesh width $dx = 1 / 20$:

<img src="./imgs/20x20-floorplan.png" style="display: block; width: 50%; margin-inline: auto;">

4. **Task 4:** Varying parameters

    1. Adjusting iterations

    > As can be seen by animating from start to finish, past iteration 5 it becomes increasingly difficult to tell any difference between iterations. <br><br>The rooms seem to settle into a stable state, which further iterations don't seem to affect very much.

    2. Adjusting $dx$

    > Naturally, it is obvious from the resulting plotted meshes that reducing $dx$ increases the number of points/cells that makes up a room. Rooms with large $dx$ look blocky, while small $dx$ yields a much smoother pattern.<br><br>It is also much more clear with smaller $dx$ where the heating and cooling sources lie. For instance with $dx = 1 / 4$, the temperatures across the rooms vary between roughly 10 and 30, whereas with $dx = 1 / 30$, the values near the border seem to much more closely match the original temperatures, 5 and 40. 
    
    3. Adjusting smoothing param

    > As expected, when you reduce the value of the smoothing parameter, it reduces the total change of temperature between iterations. For instance, setting the smoothing param to 0.9 usually results in a stable room state in around 2 or 3 iterations. When that param was reduced to 0.6, it took around 6 to 7 iterations to reach a stable state.

### Extension

1. **Task 1:** Dirichlet-Neumann matrices when mesh width dx = 1 / 3

2. **Task 2:** Is heating in the flat adequate?

3. **Task 3:** Plotted temperature distribution

    > Plot with a mesh width $dx = 1 / 100$:

<img src="./imgs/100x100-floorplan-ext.png" style="display: block; width: 50%; margin-inline: auto;">

4. **Task 4:** Varying parameters

    > Adjusting the parameters with the room extension added did not introduce any new behavior. So the same results from **Task 4** on the main assignment with three rooms were experienced even after adding the extension.

## Example Output

These two examples were created with the same initial conditions and
parameters, but demonstrate the different plotting schemes available.

<img src="./imgs/sample-heat-flow-animated.png" style="display: block; width: 50%;">

Since the "ocean" theme includes green values at the low end, the minimum
was dropped for better visual clarity.

<img src="./imgs/ocean-flow-animated.png" style="display: block; width: 50%;">

## Project Files

- **main.py** -	Project entrypoint
- **geometry.py** -	Defines rooms, their interfaces, and floorplan builders for plotting
- **matrix.py** - Construct the finite-difference matrices
- **room_solver.py** - Solve one room with given boundary conditions
- **dn_MPI.py** - Implement the Dirichlet-Neumann iteration and relaxation
- **mpi.py** - Provide MPI ranks and communication between rooms
- **plot.py** -	Plot the final temperature distribution

## Collaborator Efforts

- Lukas Nord
    - Implementation of finite difference matrix (matrix.py).
    - Main iteration for dirichlet neumann cycles (dn_MPI.py).
- Linn Preuss Jelvez
    - Implemented solver (room_solver.py).
    - Added room 4: room, interface, new floorplan.
    - Solved and plotted including room 4.      
- Orsolya Bosáková
    - Set up of the geometry of the three rooms (geometry.py)
    - Calculate the initial boundary conditions for the interfaces
- Scott Gibson
    - Plotting & Floorplan builder functions
    - Visual test file for plots

## Potential Flaws and Notes for Improvement

## TODO

- Add more unit test files
- Add Sphinx documentation support
- Add animation file save support to a constant
- General code cleanup, organization, and ensure naming convention is more convenient
- Convert from building room dimensions from dx, to building dx from room dimensions
