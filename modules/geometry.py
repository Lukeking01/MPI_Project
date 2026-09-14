import numpy as np
from .MPI import send_npdata, recv_npdata, get_rank
### apartment layout

def create_room1(dx):
    '''Initialize room 1 (1x1)
    Parameters: 
    dx : float
        Step size for the grid.
    Returns:
    U1 : ndarray
        (ny, nx) array with the initial temperatures at the boundary'''
    
    x = int(1.0/dx) + 1
    y = int(1.0/dx) + 1

    U1 = np.zeros((y, x))

    U1[0, :] = 15
    U1[-1, :] = 15
    U1[:, 0] = 40

    return U1

def create_room2(dx, include_room4=False):
    '''Initialize room 2 (1x2)
    Parameters: 
    dx : float
        Step size for the grid.
    If room4 is included: leaves interface at 0.  
    Returns:
    U2 : ndarray
        (ny, nx) array with the initial temperatures at the boundary'''
    
    x = int(1.0/dx) + 1
    y = int(2.0/dx) + 1

    U2 = np.zeros((y, x))

    middle = int(1.0/dx)

    U2[0, :] = 40
    U2[:middle, 0] = 15
    U2[-1, :] = 5
    U2[middle + 1:, -1] = 15

    if include_room4:
        half = int(0.5/dx)+1
        room4_start=middle+1
        room4_end=room4_start+half
        U2[room4_start:room4_end, -1]=0

    return U2

def create_room3(dx):
    '''Initialize room 3 (1x1)
    Parameters: 
    dx : float
        Step size for the grid.
    Returns:
    U3 : ndarray
        (ny, nx) array with the initial temperatures at the boundary'''
    
    x = int(1.0/dx) + 1
    y = int(1.0/dx) + 1

    U3 = np.zeros((y, x))

    U3[0, :] = 15
    U3[:, -1] = 40
    U3[-1, :] = 15

    return U3

def get_interfaces(U, dx):
    '''Boundary data set up with MPI communication.
    Dirichlet-Neumann set up:
        Dirichlet - rank 0 and 2 send interface temp values to rank 1.
        Neumann - rank 1 calculates the flux derivative for the interfaces and sends them to rank 0 and 2.
    Parameter:
    U : ndarray
        Temperature grid of the room.
    dx : float
        Step size for teh grid.
    Returns:
    ndarray or tuple
        rank 1 - updated room 2 with Dirichlet boundaries (walls).
        rank 0 - returns n1, the Neumann heat flux array at interface 1.
        rank 2 - returns n2, the Neumann heat flux array at interface 2.'''
    rank = get_rank()
    middle = int(1.0/dx)

    #Dirichlet boundary conditions
    if  rank == 0: #sending the right wall to rank 1
        ts = np.ascontiguousarray(U[:,-1], dtype = np.float64)
        send_npdata(ts, dest = 1)
    elif rank == 2: #sending the left wall to rank 1
        ts = np.ascontiguousarray(U[:,0], dtype = np.float64)
        send_npdata(ts, dest = 1)
    elif rank == 1:
        d1_recv = np.zeros(middle + 1, dtype=np.float64) #empty spaces to store the data
        d2_recv = np.zeros(U.shape[0] - middle, dtype=np.float64)
        recv_npdata(d1_recv, source = 0) #get values from room 1
        recv_npdata(d2_recv, source = 2) #get values from room 3
        U[:middle + 1, -1] = d2_recv #apply the values to room 2
        U[middle:, 0] = d1_recv

    #Neumann boundary conditions
    if rank == 1:
        #calculate the heat loss rate
        n1 = np.ascontiguousarray((U[:middle + 1, 1] - U[:middle + 1, 0]) / dx, dtype = np.float64)
        n2 = np.ascontiguousarray((U[middle:, -1] - U[middle:, -2]) / dx, dtype = np.float64)
        send_npdata(n1, dest=0) #sending heat values from room 1 to room 3
        send_npdata(n2, dest=2)
        return U
    elif rank == 0:
        n1 = np.zeros(middle + 1, dtype=np.float64) #space for data from room 2
        recv_npdata(n1, source=1) #recieve data from room 2
        return n1
    elif rank == 2:
        n2 = np.zeros(U.shape[0], dtype=np.float64) #space for data from room 2
        recv_npdata(n2, source=1) #recieve data from room 2
        return n2

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


def create_room4(dx):
    x= int(0.5/dx) +1
    y= int (0.5/dx) +1

    U4 = np.zeros((x,y))

    U4[-1, :]=40
    U4[:, -1]=15
    U4[0,:]=15
    return U4

def get_interface_room4(U,dx):
    """ Boundary between room2 and room4. 
    """
    rank = get_rank()
    middle = int(1.0/dx)
    half = int(0.5/dx)+1
    room4_start = middle+1
    room4_end=room4_start+half

     #Dirichlet BC
    if rank == 3:
        ts = np.ascontiguousarray(U[:,0], dtype=np.float64)
        send_npdata(ts, dest=1)
    elif rank ==1:
        d4_recv = np.zeros(room4_end-room4_start, dtype=np.float64)
        recv_npdata(d4_recv, source=3)
        U[room4_start:room4_end, -1] = d4_recv
        
    #Neumann BC
    if rank == 1:
        n4 = np.ascontiguousarray((U[room4_start:room4_end,-1]-U[room4_start:room4_end, -2])/dx,
                                   dtype=np.float64)
        send_npdata(n4,dest=3)
        return U
    elif rank == 3:
        n4 = np.zeros(room4_end-room4_start, dtype=np.float64)
        recv_npdata(n4, source=1)
        return -n4

def floorplan_addition(rooms):
    """
    :param rooms: List of 4 rooms, [left, middle, right, small_extension]
    :returns ndarray: Assignment 1 addition floorplan
    """

    [room_1, room_2, room_3, room_4] = rooms
    room_width=room_1.shape[1]

    max_room_height=max(room_2.shape[0], room_3.shape[0]+room_4.shape[0])
    floorplan_shape = (max_room_height, 3*room_width)
    floorplan = np.full(floorplan_shape, fill_value=np.nan, dtype=np.float64)

    room_offsets= [(room_2.shape[0]-room_1.shape[0],0), (0,room_width), (0,room_width*2),
                    (room_3.shape[0], room_width*2),]

    for room, (r_off,c_off) in zip(rooms,room_offsets):
        h, w = room.shape
        floorplan[r_off:r_off+h, c_off:c_off+w] = room

    return floorplan
