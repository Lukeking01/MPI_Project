# Heat Simulation with OpenMPI - Course NUMN21

In this project we aim to model the temperature distribution in an apartment by
solving the heat equation. To speed up execution of this process, we use OpenMPI
to divide the initial floorplan into multiple rooms which can be solved simultaneously.

## Usage

To run the main file, you must have OpenMPI installed, and run the following:

```
mpiexec -n 3 python main.py
```

## Output

## Project Files

- **main.py** -	Project entrypoint
- **geometry.py** -	Defines rooms, their interfaces, and floorplan builders for
plotting
- **matrix.py** - Construct the finite-difference matrices
- **room_solver.py** - Solve one room with given boundary conditions
- **dn_MPI.py** - Implement the Dirichlet-Neumann iteration and relaxation
- **mpi.py** - Provide MPI ranks and communication between rooms
- **plot.py** -	Plot the final temperature distribution

## Collaborator Efforts

- Lukas Nord
    - Item 1
    - Item 2
- Linn Preuss Jelvez
- Orsolya Bosáková
- Scott Gibson
    - Plotting & Floorplan builder functions
    - Visual test file for plots
- Mennaallah Ali Abdellatif Mohamed Alashery


## TODO
- MPI (Scotts on it) (✓)
- Make sure code is local to rooms and MPI compatible (✓)
- Testing
- init file (Check in the end)
- additional room
      - Build room
- check overall compatibility
- Modularize matrix generation
- Fuck around and find out
