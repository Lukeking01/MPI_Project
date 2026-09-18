import numpy as np

def get_room_avg(room):
    """
    Returns the average temperature across the room, after stripping out the boundaries.
    """

    return np.mean(room[1:-1, 1:-1])

def get_interval_percentage(room, min_temp, max_temp):
    """
    Returns the percentage of the room that lies within the range between the min_temp and the
    max_temp.
    """
    tmp_room = room[1:-1,1:-1]
    room_size = tmp_room.shape[0] * tmp_room.shape[1]
    room_mask = np.count_nonzero(tmp_room[(tmp_room >= min_temp) & (tmp_room <= max_temp)])

    return room_mask / room_size * 100

def log_profile(rooms, compute_time, total_iterations):
    """
    Logs data about the simulation params, timings, and potentially some numerical data 
    about the results.

    :param rooms: An array of the final room states, [room0, room1, ...]
    :param compute_time: The total time in seconds for computing the simulation, not
    including plotting.
    :param total_iterations: The total number of iterations needed to achieve a stable
    temperature distribution.
    """

    print()
    print("\t--- PROFILING ---")
    print(f"The total number of iterations needed: {total_iterations}")
    print(f"Compute time: {round(compute_time, 3)} (s)")

    print("\nAverage Temperature")
    for idx, room in enumerate(rooms):
        print(f"  Room {idx+1} - Avg: {round(get_room_avg(room), 3)} C")

    print("\nPortion of room within [18 C - 26 C]")
    for idx, room in enumerate(rooms):
        print(f"  Room {idx+1}: %{round(get_interval_percentage(room, 18, 26), 2)}")
    
    print(flush=True)