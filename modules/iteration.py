
#solve Ω2 with Dirichlet
#        ↓
#solve Ω1 and Ω3 with Neumann
#        ↓
#relax
#        ↓
#repeat
from .room_solver import room_solver as solve
from .matrix import build_matrix_neumann_right, build_rhs_neumann_right, build_matrix_neumann_left, build_rhs_neumann_left, build_internal_matrix, build_rhs_dirichlet

def solve_room3(room3, flux, nx, ny, dx):
    A = build_matrix_neumann_left(room3)
    b = build_rhs_neumann_left(room3, flux)

    solution = solve(A, b)
    room3[1:-1, 1:-1] = solution.reshape((ny, nx))

    # Reconstruct the interface boundary
    room3[:, 0] = room3[:, 1] - dx * flux

    return room3

def solve_room2(room2):

    ny = room2.shape[0] - 2
    nx = room2.shape[1] - 2

    A = build_internal_matrix(room2)

    b = build_rhs_dirichlet(
        room2,
    )

    return solve_room(room2, b, A)

def solve_room1(room1, flux, nx, ny, dx):
    A = build_matrix_neumann_right(room1)
    b = build_rhs_neumann_right(room1, flux)

    solution = solve(A, b)
    room1[1:-1, 1:-1] = solution.reshape((ny, nx))

    # Reconstruct the interface boundary
    room1[:, -1] = room1[:, -2] + dx * flux

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

