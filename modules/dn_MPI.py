
"""
Dirichlet-Neumann iteration for the multi-room heat equation.

This module implements one step of the Dirichlet-Neumann scheme and the
outer iteration loop with relaxation.  Rank 1 (room 2) is treated with Dirichlet interface conditions; ranks 0, 2 and (optionally) 3 are
treated with Neumann interface conditions.
"""

import numpy as np
from .geometry import get_interfaces, get_interface_room4
from .iteration import solve_room1, solve_room2, solve_room3, solve_room4
from .MPI import send_npdata, recv_npdata
from .constants import *

def dn_iteration(room, dx, rank, include_room4=False):
    """
    Perform a single Dirichlet-Neumann iteration for the room belonging to
    the given MPI rank.

    The algorithm follows the classic ordering:

        1. Rank 1 (room 2) receives Dirichlet data on its interfaces, optionally exchanges data with room 4, then solves a pure Dirichlet problem.
        
        2. Ranks 0, 2 (and 3) receive the corresponding Neumann fluxes and solve Neumann problems on their interfaces.

    Parameters
    ----------
    room : ndarray
        Current temperature field of the local room (including boundary values).  Shape depends on the room:
        - room 1 / room 3 : (N+1, N+1)
        - room 2          : (2N+1, N+1)
        - room 4          : (N/2+1, N/2+1)   (when include_room4=True)
    dx : float
        Mesh width.
    rank : int
        MPI rank of the calling process (0, 1, 2 or 3).
    include_room4 : bool, optional
        If True, also couple room 2 with the additional room 4 (requires four MPI ranks).  Default is False.

    Returns
    -------
    ndarray
        Updated temperature field of the local room after one iteration.
    """
    
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
            get_interface_room4(room,dx)
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
    if rank == 3:
        flux4 = -1*get_interface_room4(room,dx)[1:-1]
        room4 = solve_room4(room, flux4, nx, ny, dx)
        
        return room4

    

def dirichlet_neumann(room, dx, rank, iterations=10, omega=0.8, include_room4=False):
    """
    Run the full Dirichlet-Neumann iteration with relaxation.

    Starting from the supplied initial temperature field, the method repeatedly calls :func:`dn_iteration` and applies the relaxation

        u ← omega · u_new + (1 - omega) · u_old

    after every step.  All intermediate states are stored and returned.

    Parameters
    ----------
    room : ndarray
        Initial temperature field of the local room (including boundaries).
    dx : float
        Mesh width.
    rank : int
        MPI rank of the calling process.
    iterations : int, optional
        Number of Dirichlet-Neumann iterations to perform.  Default is 10.
    omega : float, optional
        Relaxation parameter in (0, 1].  Smaller values increase stability at the cost of slower convergence.  Default is 0.8.
    include_room4 : bool, optional
        Whether to include the optional fourth room.  Default is False.

    Returns
    -------
    ndarray
        Array of shape ``(iterations + 1, *room.shape)`` containing the
        temperature field after every iteration (index 0 is the initial
        state).
    """
    
    states = []

    states.append(
                room.copy()
                )
    
    for k in range(iterations):
        old_room = room.copy()

        new_room = dn_iteration(
            room, dx, rank, include_room4=include_room4
        )

        room = relax(new_room, old_room, omega)

        # Save a copy of this iteration
        if ANIMATE:
            states.append(
                room.copy()
            )
        elif (k == iterations-1) or (k == 0):
            states.append(
                room.copy()
            )

        # Only print once to console
        if rank == 0:
            print(f"Iteration {k+1 } finished", flush=True)
    return np.array(states)

def relax(u_new, u_old, omega):
    """
    Apply successive relaxation.

    Computes

        omega · u_new + (1 - omega) · u_old

    This damps high-frequency oscillations that can appear in the Dirichlet-Neumann iteration.

    Parameters
    ----------
    u_new : ndarray
        Solution obtained from the most recent Dirichlet or Neumann solve.
    u_old : ndarray
        Solution from the previous iteration (same shape as ``u_new``).
    omega : float
        Relaxation weight in (0, 1].  ``omega = 1`` recovers the pure
        Dirichlet-Neumann update.

    Returns
    -------
    ndarray
        Relaxed temperature field.
    """
    return omega * u_new + (1 - omega) * u_old
