
"""
Dirichlet-Neumann iteration for the multi-room heat equation.

This module implements one step of the Dirichlet-Neumann scheme and the
outer iteration loop with relaxation.  Rank 1 (room 2) is treated with Dirichlet interface conditions; ranks 0, 2 and (optionally) 3 are
treated with Neumann interface conditions.
"""

from mpi4py import MPI
import numpy as np
from .MPI import send_npdata, recv_npdata
from .geometry import exchange_dirichlet, exchange_neumann
from .room_solver import solve_room1, solve_room2, solve_room3, solve_room4
from .constants import *

def check_exit_condition(rank, new_room, old_room, include_room4):
    """
    The new_room state and old_room state for the current rank to compare. Each thread
    should compute the Matrix Norm, in this case we're choosing the Frobenius norm.
    Then all of those norms will be sent to Rank 0, which will check if each room is
    below a set threshold.

    * ranks send norm --> rank 0
    rank 0 send True/False --> * ranks

    Parameters
    rank : int
        The rank of the current running thread.
    new_room : ndarray
        New room state computed after applying smoothing parameter.
    old_room : ndarray
        Old room state to compare.
    include_room4 : bool
        Set to true if room four is included.

    Returns True if it is time to stop iterating.
    """
    
    if rank == 0:
        norm0 = np.linalg.norm(new_room - old_room)
        norm1 = np.zeros(1)
        norm2 = np.zeros(1)
        norm3 = np.zeros(1)
        
        recv_npdata(norm1, 1)
        recv_npdata(norm2, 2)
        if include_room4:
            recv_npdata(norm3, 3)

        floorplan_stable = max(norm0, norm1, norm2, norm3) < F_NORM_LIMIT
        result = np.array([floorplan_stable], dtype=bool)
        
        send_npdata(result, 1, dtype=MPI.BOOL)
        send_npdata(result, 2, dtype=MPI.BOOL)
        if include_room4:
            send_npdata(result, 3, dtype=MPI.BOOL)

        return floorplan_stable
    elif rank == 1 or rank == 2 or rank == 3:
        f_norm = np.linalg.norm(new_room - old_room)
        send_npdata(f_norm, 0)

        # Receive result from rank 0 and return
        result = np.array([False], dtype=bool)
        recv_npdata(result, 0, dtype=MPI.BOOL)
        return result[0]

def dn_iteration(room, n, rank, include_room4=False):
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

    flux = {}

    if rank == 1:
        # 1. Receive Dirichlet data from rooms 1 & 3 & 4*
        room = exchange_dirichlet(room, n, with_room4=include_room4)

        # 2. Solve room 2
        room = solve_room2(room)

        # 3. *Now* compute fluxes from the new solution and send them
        exchange_neumann(room, n, with_room4=include_room4)
        return room

    if rank == 0:
        # Send current interface temperatures
        exchange_dirichlet(room, n)
        # Receive flux that was computed *after* room 2 was solved
        flux["right"] = exchange_neumann(room, n)
        return solve_room1(room, flux)

    if rank == 2:
        exchange_dirichlet(room, n)
        flux["left"] = exchange_neumann(room, n)
        return solve_room3(room, flux)

    if rank == 3:
        exchange_dirichlet(room, n, with_room4=include_room4)
        flux["left"] = exchange_neumann(room, n, with_room4=include_room4)
        return solve_room4(room, flux)

def dirichlet_neumann(room, n, rank, iterations=10, omega=0.8, include_room4=False):
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

    Returns (tuple)
    -------
    ndarray
        Array of shape ``(iterations + 1, *room.shape)`` containing the
        temperature field after every iteration (index 0 is the initial
        state).

    int
        Number of iterations used, could be less than the requested number if the room state
        stabilizes quickly.
    """
    
    states = []

    states.append(
                room.copy()
                )
    
    for k in range(iterations):
        old_room = room.copy()

        new_room = dn_iteration(
            room, n, rank, include_room4=include_room4
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

        floorplan_stable = check_exit_condition(rank, room, old_room, include_room4)

        if floorplan_stable:
            return np.array(states), k+1
        
    return np.array(states), iterations

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
