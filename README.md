# Heat Simulation with OpenMPI - Course NUMN21

In this project we aim to model the temperature distribution in an apartment by
solving the heat equation. To speed up execution of this process, we use OpenMPI
to divide the initial floorplan into multiple rooms which can be solved simultaneously.

## Usage

To run the main file, you must have OpenMPI installed, and run the following:

```
mpiexec -n 4 python main.py
```

This runs main.py using mpiexec which should spin up three threads to handle
the computation. After a short delay, you should see a plot visualizing an
animation through the iterations of the program, and the final state it ended on.

Several aspects related to the execution and plotting can be configured in 
`/modules/constants.py`, for instance the cmap can be changed to change the color 
mapping in the heatmaps, and the animation can be toggled On/Off. Additionally you 
can control if the extension room is added, and if the boundary conditions should be 
displayed in the final plot.

## Assignment Tasks

1. **Task 1:** Dirichlet-Neumann matrices when mesh width dx = 1 / 3
   
### A matrices:

#### room 1
   >In room 1, we can see the diagonal consisting of -4 and -3 values. The -4 value comes from the Laplace equation with 2nd order central differences. The -3 value appears, because of the interior points next to the Neumann interface $\Gamma_1$. Overall, the matrix is of size 6x6.

             [[-4.  1.  0.  1.  0.  0.]
             [ 1. -4.  1.  0.  1.  0.]
             [ 1.  0. -3.  0.  0.  1.]
             [ 1.  0.  0. -4.  1.  0.]
             [ 0.  1.  0.  1. -4.  1.]
             [ 0.  0.  1.  1.  0. -3.]]

#### room 2
 >In room 2, we can see the diagonal consisting of -4 values, due to the Laplace equation. The off diagonal values of 1 are due to the connections to other interior points in the directions up, down, right or left. The size of this matrix is 12x12.

         [[-4.  1.  1.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
          [ 1. -4.  0.  1.  0.  0.  0.  0.  0.  0.  0.  0.]
          [ 1.  0. -4.  1.  1.  0.  0.  0.  0.  0.  0.  0.]
          [ 0.  1.  1. -4.  0.  1.  0.  0.  0.  0.  0.  0.]
          [ 0.  0.  1.  0. -4.  1.  1.  0.  0.  0.  0.  0.]
          [ 0.  0.  0.  1.  1. -4.  0.  1.  0.  0.  0.  0.]
          [ 0.  0.  0.  0.  1.  0. -4.  1.  1.  0.  0.  0.]
          [ 0.  0.  0.  0.  0.  1.  1. -4.  0.  1.  0.  0.]
          [ 0.  0.  0.  0.  0.  0.  1.  0. -4.  1.  1.  0.]
          [ 0.  0.  0.  0.  0.  0.  0.  1.  1. -4.  0.  1.]
          [ 0.  0.  0.  0.  0.  0.  0.  0.  1.  0. -4.  1.]
          [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  1.  1. -4.]]

#### room 3
   >Room 3 is similar to room 2, except for the order of the values on the diagonal, which in this case correspond to the other interface $\Gamma_2$. The size of the matrix is 6x6, just like in the case of room 1.

         [[-3.  0.  1.  1.  0.  0.]
          [ 1. -4.  1.  0.  1.  0.]
          [ 0.  1. -4.  0.  0.  1.]
          [ 1.  0.  0. -3.  0.  1.]
          [ 0.  1.  0.  1. -4.  1.]
          [ 0.  0.  1.  0.  1. -4.]]
         
### b vectors:

#### room 1
   >The right hand side vector for room one stores the Dirichlet boundary values combined with the Neumann flux derivatives and stores them as an array.
    
           [-55. -15. -15. -55. -15. -15.]
#### room 2
   >The vector for room 2 consists of the fixed temperature values of the outer walls and the Dirichlet values obtained from rooms 1 and 3.

           [-55. -40. -15.   0. -15. -15. -15. -15.   0. -15.  -5. -20.]
#### room 3 
   >Just as the vector for room 1, room 3 stores the Dirichlet boundary values combined with the Neumann flux derivatives.

            [-15. -15. -80. -15. -15. -80.]

### Solved matrices:

#### room 1
   > This matrix represents the heat distribution of room one after solving $Au=b$. We can see that the top and bottom values are 15 as required and the left wall is 40 due to a heater. 
 
        [[40.         15.         15.         15.        ]
          [40.         25.85306888 22.59841692 27.13823335]
          [40.         25.81385859 22.40236547 26.19718638]
          [40.         15.         15.         15.        ]]

#### room 2
   > Room 2 has 15 degrees on the upper part of the left and lower part of the right wall, as well as 40 degrees on the top due to a heater and 5 degrees because of the window on teh bottom wall. 

         [[15.         40.         40.         40.        ]
          [15.         22.37257409 18.59559567  0.        ]
          [15.         15.89470069 12.0098086   0.        ]
          [15.         14.19642005 13.54893804 15.        ]
          [15.         12.34204149 12.9895235  15.        ]
          [ 0.          7.18222239 11.06711448 15.        ]
          [ 0.          5.3197336   9.09671202 15.        ]
          [ 5.          5.          5.          5.        ]]

#### room 3 
   > Room 3 has two regular walls on the top and bottom with 15 degrees and a heater on the right wall of 40 degrees.

        [[15.         15.         15.         40.        ]
          [42.98666006 31.46770123 37.10968436 40.        ]
          [39.65910449 30.77446048 36.97103621 40.        ]
          [15.         15.         15.         40.        ]]

3. **Task 2:** Is heating in the flat adequate?

   > The heating in the flat should be inspected by each room individually. In room 1 and 3 the temperature moves in the interval from 19 to 25 degrees, which can be considered comfortably warm. However, in the case of room 2, the internal tempeture on the lower end of the room seems to drop below 15 degrees, which is due to the window creating a cold zone. Unless this temperature is tempting for someone, maybe insulating that window could be a good solution. 

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

### A matrices:

#### room 2

   > The room 2 A matrix looks similar to the one we had in the original part of Project 1. Except for a slight shift of the placement of the -4 and 1 values, due to the interaction with room 4. 

      [[-4.  1.  1.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
       [ 1. -4.  0.  1.  0.  0.  0.  0.  0.  0.  0.  0.]
       [ 1.  0. -4.  1.  1.  0.  0.  0.  0.  0.  0.  0.]
       [ 0.  1.  1. -4.  0.  1.  0.  0.  0.  0.  0.  0.]
       [ 0.  0.  1.  0. -4.  1.  1.  0.  0.  0.  0.  0.]
       [ 0.  0.  0.  1.  1. -4.  0.  1.  0.  0.  0.  0.]
       [ 0.  0.  0.  0.  1.  0. -4.  1.  1.  0.  0.  0.]
       [ 0.  0.  0.  0.  0.  1.  1. -4.  0.  1.  0.  0.]
       [ 0.  0.  0.  0.  0.  0.  1.  0. -4.  1.  1.  0.]
       [ 0.  0.  0.  0.  0.  0.  0.  1.  1. -4.  0.  1.]
       [ 0.  0.  0.  0.  0.  0.  0.  0.  1.  0. -4.  1.]
       [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  1.  1. -4.]]

#### room 4

   > Due to the lack of internal points in room 2 in the case dx=1/3, the matrix A is empty and we chose not to display it.

### b vector:

### room 2 

      [-55. -40. -15.   0. -15. -15. -15. -15.   0. -15.  -5. -20.]

#### room 4

   > For the same reason as for matrix A, the b vector is not displayed.

### Solved matrices:

#### room 1

   > In room 1, we can see that the top and bottom values are 15 as required and the left wall is 40 due to a heater. The internal values are between 25 and 19 degrees approximately, which match the corresponding values in room 2.

     [[40.         15.         15.         15.        ]
       [40.         25.85306888 22.59841692 27.13823335]
       [40.         25.81385859 22.40236547 26.19718638]
       [40.         15.         15.         15.        ]]

#### room 2

   > Room 2 has 15 degrees on the upper part of the left, as well as 40 degrees on the top due to a heater and 5 degrees because of the window on teh bottom wall. The interior values range from 14 to 39 degrees, with interface values matching those of room 1, 3 and 4.

      [[15.         40.         40.         40.        ]
       [15.         22.37257409 18.59559567  0.        ]
       [15.         15.89470069 12.0098086   0.        ]
       [15.         14.19642005 13.54893804 15.        ]
       [15.         12.34204149 12.9895235  15.        ]
       [ 0.          7.18222239 11.06711448 15.        ]
       [ 0.          5.3197336   9.09671202 15.        ]
       [ 5.          5.          5.          5.        ]]

#### room 3

   > Room 3 has two regular walls on the top and bottom with 15 degrees and a heater on the right wall of 40 degrees. The internal temperatures are approximately 24, 20 and 19 degrees. The interface values on the right match those of room 2 as expected.

      [[15.         15.         15.         40.        ]
       [42.98666006 31.46770123 37.10968436 40.        ]
       [39.65910449 30.77446048 36.97103621 40.        ]
       [15.         15.         15.         40.        ]]

#### room 4

   > Room 4 does not have any internal points to discuss, however the values of the interface between room 2 and 4 match approximately.

      [[15. 15.]
       [40. 40.]]

3. **Task 2:** Is heating in the flat adequate?

   > The heating in the flat should be inspected by each room individually. In room 1 and 3 the temperature moves in the interval from 19 to 25 degrees, which can be considered comfortably warm. However, in the case of room 2, the internal tempeture on the lower end of the room seems to drop below 15 degrees to 14 degrees, which is due to the window creating a cold zone. Additionally, we have almost 40 degrees on the interface with room 4, making it rather warm in that area. The best idea would be to isolate the window in room 2 and turn down the heating in room 4 for a more comfortable environment.

5. **Task 3:** Plotted temperature distribution

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

- **__init__.py** - Modules entrypoint, collects all internal dependencies
- **constants.py** - Defines customization for simulation params
- **dn_MPI.py** - Implement the Dirichlet-Neumann iteration and relaxation
- **geometry.py** -	Defines rooms, their interfaces, and floorplan builders for plotting
- **iteration.py** - Extension of the room_solver
- **room_solver.py** - Solve one room with given boundary conditions
- **matrix.py** - Construct the finite-difference matrices (LHS, RHS)
- **MPI.py** - Provide MPI ranks and communication between rooms
- **plot.py** - Plot the final temperature distribution

## Creating HTML Documentation

In this project we have Sphinx setup to generate docs on command. To generate docs and view them,
follow these steps:

1. Change to the \docs directory: `cd docs`
2. Run the build command: `.\make html`
3. Wait for the build to finish, the generated html docs should populate the \docs\build folder
or create one if none existed.
4. Open the `index.html` file in a server or in your browser to view the output.

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

- (DONE!) Convert from building room dimensions from dx, to building dx from room dimensions
- Remove the need for an iteration count. Determine a good hueristic to compare the rooms delta between iterations. If the change is below a threshold after smoothing, then consider the solution stable and return the solution along with how many iterations it took. 
- Display quantitative analysis of temperature distribution on each room and some metric to display comparing all rooms as a whole.
- Add animation file save support to a constant.
- Add console params to override constants for room size, omega value, and if the extension should be included
