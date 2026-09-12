
#solve Ω2 with Dirichlet
#        ↓
#solve Ω1 and Ω3 with Neumann
#        ↓
#relax
#        ↓
#repeat
import numpy as np
from geometry import get_interfaces
from iteration import solve_room1, solve_room2, solve_room3
from MPI import send_npdata, recv_npdata

def dn_iteration(room, dx, rank):

    
    nx = room.shape[1] - 2
    ny = room.shape[0] - 2
    

    # -----------------------------------------
    # 1. Update Room 2's interface temperatures
    # -----------------------------------------
    
    ## TODO
    ## This needs to be altered using MPI
    room2, _, _ = get_interfaces(
        room1,
        room2,
        room3,
        dx
    )
    

    if rank == 1:
        room = room2
        # -----------------------------------------
        # 2. Solve Room 2 with Dirichlet conditions
        # -----------------------------------------

        room = solve_room2(room)

        # -----------------------------------------
        # 3. Calculate fluxes from Room 2
        # -----------------------------------------

        flux1 = -1 * (
            room[1:nx+1, 1] -
            room[1:ny+1, 0]
        ) / dx
        
        send_npdata(flux1,0)
        
        flux3 = -1 * (
            room[nx+2:-1, -1] -
            room[ny+2:-1, -2]
        ) / dx

        send_npdata(flux3,2)
        return room
        
    if rank == 0:
        # -----------------------------------------
        # 4. Solve Room 1 with Neumann
        # -----------------------------------------
        flux1 = np.empty(ny)
        recv_npdata(flux1,1)
        
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
        flux3 = np.empty(ny)
        recv_npdata(flux3,1)
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

    
    
    for k in range(iterations):
        
        room = room.copy()

        new_room = dn_iteration(
            room, dx, rank
        )
        
        states.append(
                        room.copy()
                        )

        room = relax(new_room, room, omega)

        # Save a copy of this iteration
        states.append(
            room.copy()
        )

    return states

def relax(u_new, u_old, omega):
    """
        Apply relaxation:
        u_new <- omega * u_new + (1 - omega) * u_old
    """
    return omega * u_new + (1 - omega) * u_old
