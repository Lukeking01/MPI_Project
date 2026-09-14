
#solve Ω2 with Dirichlet
#        ↓
#solve Ω1 and Ω3 with Neumann
#        ↓
#relax
#        ↓
#repeat
import numpy as np
from .geometry import get_interfaces, get_interface_room4
from .iteration import solve_room1, solve_room2, solve_room3, solve_room4
from .MPI import send_npdata, recv_npdata

def dn_iteration(room, dx, rank, include_room4=False):

    
    nx = room.shape[1] - 2
    ny = room.shape[0] - 2

    middle = int(1.0/dx)
    half = int(0.5/dx) + 1
    room4_start = middle + 1
    room4_end = room4_start + half

    if rank == 1:
        # -----------------------------------------
        # 1. Update Room 2's interface temperatures and send fluxes
        # -----------------------------------------
        room = get_interfaces(room,dx)
        # -----------------------------------------
        # 2. Solve Room 2 with Dirichlet conditions
        # -----------------------------------------

        if include_room4:
            print(f"DEBUG before room4 interface: {room[room4_start:room4_end, -1]}", flush=True)
            get_interface_room4(room,dx)
            print(f"DEBUG after room4 interface: {room[room4_start:room4_end, -1]}", flush=True)

        room = solve_room2(room)
        print(f"DEBUG room2 min/max: {room.min():.2f}, {room.max():.2f}", flush=True)
       

        return room
        
    if rank == 0:
        # -----------------------------------------
        # 4. Solve Room 1 with Neumann
        # -----------------------------------------
        flux1 = get_interfaces(room,dx)[1:-1]
        
        room1 = solve_room1(
            room,
            flux1,
            nx,
            ny,
            dx
        )
        return room1

    if rank == 2:
        # -----------------------------------------
        # 5. Solve Room 3 with Neumann
        # -----------------------------------------
        flux3 = get_interfaces(room,dx)[1:-1]
        room3 = solve_room3(
            room,
            flux3,
            nx,
            ny,
            dx
        )
        return room3
    if rank == 3:
        flux4 = get_interface_room4(room,dx)[1:-1]
        room4 = solve_room4(room, flux4, nx, ny, dx)
        print(f"DEBUG room4 min/max: {room4.min():.2f}, {room4.max():.2f}", flush=True)
        
        return room4

    

def dirichlet_neumann(room, dx, rank, iterations=10, omega=0.8, include_room4=False):
    states = []

    states.append(
                room.copy()
                )
    
    for k in range(iterations):
        
        room = room.copy()

        new_room = dn_iteration(
            room, dx, rank, include_room4=include_room4
        )

        room = relax(new_room, room, omega)

        # Save a copy of this iteration
        states.append(
            room.copy()
        )

    return np.array(states)

def relax(u_new, u_old, omega):
    """
        Apply relaxation:
        u_new <- omega * u_new + (1 - omega) * u_old
    """
    return omega * u_new + (1 - omega) * u_old
