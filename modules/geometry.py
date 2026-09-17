import numpy as np
from .MPI import send_npdata, recv_npdata, get_rank
from .constants import *

### ROOM BUILDERS ###

def create_room1(n):
    '''Initialize room 1 (1x1)
    Parameters: 
    dx : float
        Step size for the grid.
    Returns:
    U1 : ndarray
        (ny, nx) array with the initial temperatures at the boundary'''
    
    dx = int(1.0/n)

    U1 = np.zeros((n, n)) + FLOOR_TEMP

    U1[0, :] = WALL_TEMP
    U1[-1, :] = WALL_TEMP
    U1[:, 0] = HEATER_TEMP

    return U1

def create_room2(n, include_room4=False):
    '''Initialize room 2 (1x2)
    Parameters: 
    dx : float
        Step size for the grid.
    If room4 is included: leaves interface at 0.  
    Returns:
    U2 : ndarray
        (ny, nx) array with the initial temperatures at the boundary'''
    
    dx = int(1.0/n)

    U2 = np.zeros((2*n, n)) + FLOOR_TEMP

    middle = n

    U2[middle-1:, -1] = WALL_TEMP
    U2[:middle+1, 0] = WALL_TEMP
    U2[-1, :] = WINDOW_TEMP
    
    U2[0, :] = HEATER_TEMP

    if include_room4:
        half = int(n/2)
        room4_start=n
        room4_end=room4_start+half
        U2[room4_start:room4_end, -1]=WALL_TEMP
        U2[room4_start+1:room4_end-1, -1]=FLOOR_TEMP

    return U2

def create_room3(n):
    '''Initialize room 3 (1x1)
    Parameters: 
    dx : float
        Step size for the grid.
    Returns:
    U3 : ndarray
        (ny, nx) array with the initial temperatures at the boundary'''
    
    dx = int(1.0/n)

    U3 = np.zeros((n, n)) + FLOOR_TEMP
    
    U3[-1, :] = WALL_TEMP
    U3[0, :] = WALL_TEMP
    U3[:, -1] = HEATER_TEMP
    
    return U3

def create_room4(n):
    '''Initialize room 4 (1/2x1/2)
    Parameters: 
    dx : float
        Step size for the grid.
    Returns:
    U4 : ndarray
        (ny, nx) array with the initial temperatures at the boundary'''

    half = int(n / 2)
    U4 = np.zeros((half,half)) + FLOOR_TEMP

    U4[:, -1]=WALL_TEMP
    U4[0,:]=WALL_TEMP
    U4[-1, :]=HEATER_TEMP
    return U4

### BOUNDARY CONDITIONS ###



def exchange_dirichlet(U, n, with_room4 = False):
    '''Exchange Dirichlet interface temperatures.
    Rank 0 and 2 send their interface temps to rank 1.
    Rank 1 receives and applies them to room 2 interfaces.

    Returned room matrices only change if they received new data.
    '''
    rank = get_rank()
    middle = n

    if rank == 0:  # sending the right wall to rank 1
        ts = np.ascontiguousarray(U[1:-1, -1], dtype=np.float64)
        send_npdata(ts, dest=1)
    elif rank == 2:  # sending the left wall to rank 1
        ts = np.ascontiguousarray(U[1:-1, 0], dtype=np.float64)
        send_npdata(ts, dest=1)
    elif rank == 3 and with_room4: # sending the left wall to rank 1
        ts = np.ascontiguousarray(U[1:-1, 0], dtype=np.float64)
        send_npdata(ts, dest=1)
    elif rank == 1: # Receive and update data in room 2
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


def exchange_neumann(U, n):
    '''Compute and exchange Neumann fluxes *after* room 2 has been solved.
    Rank 1 computes fluxes from its updated solution and sends them.
    Rank 0 / 2 receive the fluxes.
    '''
    rank = get_rank()
    middle = n

    if rank == 1:
        # lower-left interface (shared with room 1)
        # outward normal of room 2 points left → send opposite for room 1
        n1 = np.ascontiguousarray(
            (U[middle + 1:-1, 1] - U[middle + 1:-1, 0]) / DX, dtype=np.float64
        )
        # upper-right interface (shared with room 3)
        n2 = np.ascontiguousarray(
            (U[1:middle - 1, -2] - U[1:middle - 1, -1]) / DX, dtype=np.float64
        )
        send_npdata(n1, dest=0)
        send_npdata(n2, dest=2)
        return U
    elif rank == 0:
        n1 = np.zeros(n - 2, dtype=np.float64)
        recv_npdata(n1, source=1)
        return n1
    elif rank == 2:
        n2 = np.zeros(n - 2, dtype=np.float64)
        recv_npdata(n2, source=1)
        return n2
    return U

def get_interface_room4(U,dx):
    '''Boundary data between rooms 2 and 4 set up with MPI communication.

    --- REPLACE THE FOLLOWING ---
    Dirichlet-Neumann set up:
        Dirichlet - rank 3 sends interface temp values to rank 1.
        Neumann - rank 1 calculates the flux derivative for the interface and sends them to rank 3.
    Parameter:
    U : ndarray
        Temperature grid of the room.
    dx : float
        Step size for the grid.
    Returns:
    ndarray or tuple
        rank 1 - updated room 2 with Dirichlet boundary (walls).
        rank 0 - returns n3, the Neumann heat flux array at interface 4.
        rank 3 - ...'''
    rank = get_rank()
    middle = int(1.0/dx)
    half = int(0.5/dx)+1
    room4_start = middle+1
    room4_end=room4_start+half

     #Dirichlet BC
    if rank == 3:
        ts = np.ascontiguousarray(U[:,0], dtype=np.float64)
        send_npdata(ts, dest=1)
    elif rank == 1:
        d4_recv = np.zeros(room4_end-room4_start, dtype=np.float64)
        recv_npdata(d4_recv, source=3)
        U[room4_start:room4_end, -1] = d4_recv
        
    #Neumann BC
    if rank == 1:
        n4 = np.ascontiguousarray((U[room4_start:room4_end,-1]-U[room4_start:room4_end, -2]),
                                   dtype=np.float64)
        send_npdata(n4,dest=3)
        return U
    elif rank == 3:
        n4 = np.zeros(room4_end-room4_start, dtype=np.float64)
        recv_npdata(n4, source=1)
        return -n4

### FLOORPLAN BUILDERS ###

def floorplan_main(rooms):
    """
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
    :param rooms: List of 4 rooms, [left, middle, right, small_extension]
    :returns ndarray: Assignment 1 addition floorplan
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
