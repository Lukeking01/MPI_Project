
#solve Ω2 with Dirichlet
#        ↓
#solve Ω1 and Ω3 with Neumann
#        ↓
#relax
#        ↓
#repeat
from room_solver import solve_dirichlet as solve
import geometry as geo
from matrix import build_matrix_neumann_right, build_rhs_neumann_right, build_matrix_neumann_left, build_rhs_neumann_left, build_internal_matrix, build_rhs_dirichlet

def dn_iteration(room1, room2, room3, dx):

    nx1 = room1.shape[1] - 2
    ny1 = room1.shape[0] - 2

    nx2 = room2.shape[1] - 2
    ny2 = room2.shape[0] - 2

    nx3 = room3.shape[1] - 2
    ny3 = room3.shape[0] - 2

    # -----------------------------------------
    # 1. Update Room 2's interface temperatures
    # -----------------------------------------

    room2, _, _ = geo.get_interfaces(
        room1,
        room2,
        room3,
        dx
    )

    # -----------------------------------------
    # 2. Solve Room 2 with Dirichlet conditions
    # -----------------------------------------

    room2 = solve_room2(room2)

    # -----------------------------------------
    # 3. Calculate fluxes from Room 2
    # -----------------------------------------

    flux1 = -1 * (
        room2[1:ny1+1, 1] -
        room2[1:ny1+1, 0]
    ) / dx

    flux3 = -1 * (
        room2[ny3+2:-1, -1] -
        room2[ny3+2:-1, -2]
    ) / dx

    # -----------------------------------------
    # 4. Solve Room 1 with Neumann
    # -----------------------------------------

    room1 = solve_room1(
        room1,
        flux1,
        nx1,
        ny1,
        dx
    )

    # -----------------------------------------
    # 5. Solve Room 3 with Neumann
    # -----------------------------------------

    room3 = solve_room3(
        room3,
        flux3,
        nx3,
        ny3,
        dx
    )

    return room1, room2, room3

def dirichlet_neumann(room1, room2, room3, dx, iterations=10, omega=0.8):
    states = []

    for k in range(iterations):
        old_room1 = room1.copy()
        old_room2 = room2.copy()
        old_room3 = room3.copy()

        new_room1, new_room2, new_room3 = dn_iteration(
            room1, room2, room3, dx
        )

        room1 = relax(new_room1, old_room1, omega)
        room2 = relax(new_room2, old_room2, omega)
        room3 = relax(new_room3, old_room3, omega)

        # Save a copy of this iteration
        states.append((
            room1.copy(),
            room2.copy(),
            room3.copy()
        ))

    return room1, room2, room3, states

def relax(u_new, u_old, omega):
    """
        Apply relaxation:
        u_new <- omega * u_new + (1 - omega) * u_old
    """
    return omega * u_new + (1 - omega) * u_old

def solve_room3(room3, flux, nx, ny, dx):
    A = build_matrix_neumann_left(nx, ny)
    b = build_rhs_neumann_left(room3, flux, nx, ny)

    solution = solve(A, b)
    room3[1:-1, 1:-1] = solution.reshape((ny, nx))

    # Reconstruct the interface boundary
    room3[1:-1, 0] = room3[1:-1, 1] - dx * flux

    return room3

def solve_room2(room2):

    ny = room2.shape[0] - 2
    nx = room2.shape[1] - 2

    A = build_internal_matrix(nx, ny)

    b = build_rhs_dirichlet(
        room2,
        nx,
        ny
    )

    return solve_room(room2, b, A)

def solve_room1(room1, flux, nx, ny, dx):
    A = build_matrix_neumann_right(nx, ny)
    b = build_rhs_neumann_right(room1, flux, nx, ny)

    solution = solve(A, b)
    room1[1:-1, 1:-1] = solution.reshape((ny, nx))

    # Reconstruct the interface boundary
    room1[1:-1, -1] = room1[1:-1, -2] + dx * flux

    return room1

def solve_room(room, rhs, A):
    """
    Solve A u = b and put the solution into
    the interior of the room.
    """

    ny = room.shape[0] - 2
    nx = room.shape[1] - 2

    solution = solve(A, rhs)

    room[1:-1, 1:-1] = solution.reshape((ny, nx))

    return room

