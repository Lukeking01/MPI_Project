import numpy as np
from .MPI import send_npdata, recv_npdata, get_rank
from .constants import *

### ROOM BUILDERS ###

def init_room_state(size):
    """
    Creates a new ndarray with given size, initializing all values to the floor
    temperature.

    Parameters:
    size : tuple
        The dimensions to make the ndarray for the room.
    Returns:
    U_init : ndarray
        Initial room state.
    """
    
    U_init = np.zeros(size) + FLOOR_TEMP
    return U_init

def create_room1(n):
    """
    Initialize room 1 (1x1)

    Parameters: 
    n : int
        Number of room subdivisions in a single dimension.
    Returns:
    U1 : ndarray
        (ny, nx) array with the initial temperatures at the boundary
    """
    
    U1 = init_room_state((n, n))
    U1[0, :] = WALL_TEMP     # Top wall
    U1[-1, :] = WALL_TEMP    # Bottom wall
    U1[:, 0] = HEATER_TEMP   # Left wall

    return U1

def create_room2(n, include_room4=False):
    """
    Initialize room 2 (1x2)

    Parameters: 
    n : int
        Number of room subdivisions in a single dimension.
    include_room4 : bool
        Sets custom boundary condition on right edge if the extension is included.
        Leaves interface at 0.
    Returns:
    U2 : ndarray
        (ny, nx) array with the initial temperatures at the boundary
    """

    U2 = init_room_state((2*n, n))

    middle = n

    U2[0, :] = HEATER_TEMP          # Top wall
    U2[middle-1:, -1] = WALL_TEMP   # Lower right wall
    U2[:middle+1, 0] = WALL_TEMP    # Upper left wall
    U2[-1, :] = WINDOW_TEMP         # Bottom wall

    if include_room4:
        # Extension room
        half = int(n/2)
        room4_start=n
        room4_end=room4_start+half
        U2[room4_start:room4_end, -1]=WALL_TEMP
        U2[room4_start+1:room4_end-1, -1]=FLOOR_TEMP

    return U2

def create_room3(n):
    """
    Initialize room 3 (1x1)

    Parameters: 
    n : int
        Number of room subdivisions in a single dimension.
    Returns:
    U3 : ndarray
        (ny, nx) array with the initial temperatures at the boundary
    """

    U3 = init_room_state((n, n))
    U3[-1, :] = WALL_TEMP
    U3[0, :] = WALL_TEMP
    U3[:, -1] = HEATER_TEMP
    
    return U3

def create_room4(n):
    """
    Initialize room 3 (0.5x0.5)

    Parameters: 
    n : int
        Number of room subdivisions in a single dimension.
    Returns:
    U4 : ndarray
        (ny, nx) array with the initial temperatures at the boundary
    """

    half = int(n / 2)
    U4 = init_room_state((half, half))
    U4[:, -1]=WALL_TEMP
    U4[0,:]=WALL_TEMP
    U4[-1, :]=HEATER_TEMP

    return U4


### BOUNDARY CONDITIONS ###

def exchange_dirichlet(U, n, with_room4 = False):
    """
    Exchange Dirichlet interface temperatures.

    Ranks 0, 2, 4* send their interface temps to rank 1.
    Rank 1 receives and applies them to room 2 interfaces.

    Parameters:
    U : ndarray
        Input room for the rank calling this function.
    n : int
        Number of room subdivisions in a single dimension.
    with_room4 : bool
        Whether or not to include room 4 boundaries. This only effects rooms 2 and 4.

    Returns:
    ndarray reflecting the updated room state with new boundary information. Note, only
    rooms receiving new Dirichlet conditions will return an updated room state.
    """

    rank = get_rank()
    middle = n

    if rank == 0:
        # Room 1 sends the right wall to room 2
        ts = np.ascontiguousarray(U[1:-1, -1], dtype=np.float64)
        send_npdata(ts, dest=1)
    elif rank == 2:
        # Room 3 sends the left wall to room 2
        ts = np.ascontiguousarray(U[1:-1, 0], dtype=np.float64)
        send_npdata(ts, dest=1)
    elif rank == 3 and with_room4:
        # Room 4 sends the left wall to room 2
        ts = np.ascontiguousarray(U[1:-1, 0], dtype=np.float64)
        send_npdata(ts, dest=1)
    elif rank == 1: 
        # Receive and update data in room 2
        
        # From room 1 (lower-left interface)
        d1_recv = np.zeros(n - 2, dtype=np.float64)
        recv_npdata(d1_recv, source=0)
        U[middle + 1:-1, 0] = d1_recv
        
        # From room 3 (upper-right interface)
        d2_recv = np.zeros(n - 2, dtype=np.float64)
        recv_npdata(d2_recv, source=2)
        U[1:middle - 1, -1] = d2_recv

        # From room 4 (midle-right interface)
        if with_room4:
            interface_len = int(n / 2) - 2
            d3_recv = np.zeros(interface_len, dtype=np.float64)
            recv_npdata(d3_recv, source=3)
            U[middle+1:middle+interface_len+1, -1] = d3_recv
    
    # Return room state for all ranks
    return U


def exchange_neumann(U, n, with_room4 = False):
    """
    Compute and exchange Neumann fluxes *after* room 2 has been solved.

    Rank 1 computes fluxes from its updated solution and sends them.
    Rank 0 / 2 / 4* receive the fluxes.

    Parameters:
    U : ndarray
        Input room for the rank calling this function.
    n : int
        Number of room subdivisions in a single dimension.
    with_room4 : bool
        Whether or not to include room 4 boundaries. This only effects rooms 2 and 4.

    Returns:
    When called by room 2, which is only sending fluxes, returns None.

    When called by the rooms receiving Neumann conditions, an ndarray of flux values
    describing the boundary they share with room 2 is returned.
    """

    rank = get_rank()
    middle = n

    if rank == 1:
        # lower-left interface (shared with room 1)
        # outward normal of room 2 points left → send opposite for room 1
        n1 = np.ascontiguousarray(
            (U[middle + 1:-1, 1] - U[middle + 1:-1, 0]) / DX, dtype=np.float64
        )
        send_npdata(n1, dest=0)
        
        # upper-right interface (shared with room 3)
        n2 = np.ascontiguousarray(
            (U[1:middle - 1, -2] - U[1:middle - 1, -1]) / DX, dtype=np.float64
        )
        send_npdata(n2, dest=2)

        if with_room4:
            inter_start = middle + 1
            inter_end = middle + int(n / 2) - 1
            
            # middle-right interface (shared with room 3)
            n3 = np.ascontiguousarray(
                (U[inter_start:inter_end, -2] - U[inter_start:inter_end, -1]) / DX, dtype=np.float64
            )
            send_npdata(n3, dest=3)
    elif rank == 0:
        # Room 1, receives flux
        flux1 = np.zeros(n - 2, dtype=np.float64)
        recv_npdata(flux1, source=1)
        return flux1
    elif rank == 2:
        # Room 3, receives flux
        flux2 = np.zeros(n - 2, dtype=np.float64)
        recv_npdata(flux2, source=1)
        return flux2
    elif rank == 3 and with_room4:
        # Room 4, receives flux
        flux3 = np.zeros(int(n / 2) - 2, dtype=np.float64)
        recv_npdata(flux3, source=1)
        return flux3


### FLOORPLAN BUILDERS ###

def floorplan_main(rooms):
    """
    Constructs an ndarray floorplan of the assignment rooms stitched together.
    
    :param rooms: List of 3 rooms, [left, middle, right]
    :returns ndarray: Assignment 1 floorplan
    """
    [room_1, room_2, room_3] = rooms

    # Assuming that each room has equal width and room_2 is the tallest:
    max_room_height = room_2.shape[0]
    room_width = room_1.shape[1]

    # Smallest shape for a box that can fit the full floorplan.
    floorplan_shape = (max_room_height, 3 * room_width)

    # Start with a blank canvas
    floorplan = np.full(floorplan_shape, fill_value=np.nan, dtype=np.float64)

    # Create list of (r, c) room offsets
    room_offsets = [
        (room_2.shape[0] - room_1.shape[0], 0),
        (0, room_width),
        (0, room_width * 2),
    ]

    for room, (r_off, c_off) in zip(rooms, room_offsets):
        h, w = room.shape
        # Insert room at the correct offset
        floorplan[r_off:r_off + h, c_off:c_off + w] = room

    return floorplan

def floorplan_addition(rooms):
    """
    Constructs an ndarray floorplan of the assignment rooms plus the extension
    stitched together.

    :param rooms: List of 4 rooms, [left, middle, right, small_extension]
    :returns ndarray: Assignment 1 extension floorplan
    """
    
    [room_1, room_2, room_3, room_4] = rooms
    
    # Assuming that each room has equal width and room_2 is the tallest:
    max_room_height = room_2.shape[0]
    room_width = room_1.shape[1]

    # Smallest shape for a box that can fit the full floorplan.
    floorplan_shape = (max_room_height, 3 * room_width)

    # Start with a blank canvas
    floorplan = np.full(floorplan_shape, fill_value=np.nan, dtype=np.float64)

    # Create list of (r, c) room offsets
    room_offsets = [
        (room_2.shape[0] - room_1.shape[0], 0),
        (0, room_width),
        (0, room_width * 2),
        (room_3.shape[0], room_width * 2) if not CROP else (room_3.shape[0] + 2, room_width * 2),
    ]

    for room, (r_off, c_off) in zip(rooms, room_offsets):
        h, w = room.shape
        # Insert room at the correct offset
        floorplan[r_off:r_off + h, c_off:c_off + w] = room

    return floorplan
