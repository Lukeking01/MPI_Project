
#solve Ω2 with Dirichlet
#        ↓
#solve Ω1 and Ω3 with Neumann
#        ↓
#relax
#        ↓
#repeat
import numpy as np
from .geometry import get_interfaces
from .iteration import solve_room1, solve_room2, solve_room3
from .MPI import send_npdata, recv_npdata

def dn_iteration(room, dx, rank):

    
    nx = room.shape[1] - 2
    ny = room.shape[0] - 2

    if rank == 1:
        # -----------------------------------------
        # 1. Update Room 2's interface temperatures and send fluxes
        # -----------------------------------------
        room = get_interfaces(room,dx)
        # -----------------------------------------
        # 2. Solve Room 2 with Dirichlet conditions
        # -----------------------------------------

        room = solve_room2(room)

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
        flux3 = -1*get_interfaces(room,dx)[1:-1]
        room3 = solve_room3(
            room,
            flux3,
            nx,
            ny,
            dx
        )
        return room3

    

def dirichlet_neumann(room, dx, rank, iterations=10, omega=0.8):
    states = []

    states.append(
                room.copy()
                )
    
    for k in range(iterations):
        
        room = room.copy()

        new_room = dn_iteration(
            room, dx, rank
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
