import numpy as np
import time

# Import all modules and constants
from modules import *

def main():
    rank = get_rank()

    # Track starting time to display the total runtime for this simulation.
    start_time = time.time()

    # Early return for all threads that exceed the number of rooms
    total_rooms = 3 if not INCLUDE_ROOM4 else 4
    if rank >= total_rooms:
        return
    
    # Initialize room states
    if rank == 0:
        room = create_room1(DX)
    if rank == 1:
        room = create_room2(DX, include_room4=INCLUDE_ROOM4)
    if rank == 2:
        room = create_room3(DX)
    if INCLUDE_ROOM4 and rank == 3:
        room = create_room4(DX)

    # Run simulation with all params
    solution = dirichlet_neumann(
        room,
        dx = DX,
        rank = rank,
        iterations = N_ITERATIONS,
        omega = OMEGA,
        include_room4=INCLUDE_ROOM4
        )

    # For all ranks other than 0, send output data to rank 0 for display
    if rank == 1 or rank == 2 or rank == 3:
        send_npdata(solution, 0)
    
    if rank == 0:
        # Note, all these rooms are being used for is to get the dimensions of each room,
        # that can certainly be made more efficient by not building the full rooms.
        room2 = create_room2(DX, include_room4=INCLUDE_ROOM4)
        room3 = create_room3(DX)

        sol_frame_count = solution.shape[0]

        # Set up empty arrays to receive simulation data from other ranks
        data2 = np.empty(
            (sol_frame_count, *room2.shape),
            dtype=float
        )
        data3 = np.empty(
            (sol_frame_count, *room3.shape),
            dtype=float
        )

        recv_npdata(data2, 1)
        recv_npdata(data3, 2)

        # Collect all rooms into a single "data" array and choose custom floorplan builder function 
        # depending on if the addition is included.
        if not INCLUDE_ROOM4:
            data = [[solution[i],data2[i],data3[i]] for i in range(solution.shape[0])]
            floorplan_builder=floorplan_main
        else:
            room4=create_room4(DX)
            data4=np.empty((sol_frame_count, *room4.shape), dtype=float)
            recv_npdata(data4, 3)
            data=[[solution[i], data2[i], data3[i], data4[i]] for i in range(solution.shape[0])]
            floorplan_builder = floorplan_addition

        # Crop room boundary conditions if necessary
        if CROP:
            data = [[room[1:-1,1:-1] for room in rooms] for rooms in data]
        # Omit the first starting condition frame when animate is set to False, shows the initial state 
        # as the state after a single iteration, which looks a bit nicer than the starting conditions.
        if not ANIMATE:
            data = data[1:]

        def log_profile(compute_time):
            """
            Logs data about the simulation params, timings, and potentially some numerical data 
            about the results.
            TODO

            :param compute_time: The total time in seconds for computing the simulation, not
            including plotting.
            """
            pass

        total_time = time.time() - start_time
        log_profile(total_time)

        # Plot the temperature distribution
        plot_temperature(
            data, 
            floorplan_builder=floorplan_builder, 
            show_animation=ANIMATE,
            **PLOT_PARAMS,
            animation_params=DEFAULT_ANIMATION_PARAMS,
        )



if __name__ == "__main__":
    main()
