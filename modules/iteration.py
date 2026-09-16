
#solve Ω2 with Dirichlet
#        ↓
#solve Ω1 and Ω3 with Neumann
#        ↓
#relax
#        ↓
#repeat
from .room_solver import room_solver as solve
from .matrix import build_matrix_neumann_right, build_rhs_neumann_right, build_matrix_neumann_left, build_rhs_neumann_left, build_internal_matrix, build_rhs_dirichlet

# Save the A matrices between iterations
A1_cache = None
A2_cache = None
A3_cache = None
A4_cache = None

### Solvers ###
# 1. Build the LHS sparse matrix A
# 2. Build the RHS matrix b
# 3. Run the sparse solver

def solve_room(room, rhs, A):
    """
    Solve A u = b and put the solution into
    the interior of the room.
    """

    ny = room.shape[0] - 2
    nx = room.shape[1] - 2

    solution = solve(A.tocsc(), rhs)

    room[1:-1, 1:-1] = solution.reshape((ny, nx))

    return room


def solve_room3(room3, flux, nx, ny, dx):
    global A3_cache
    
    A = A3_cache if A3_cache != None else build_matrix_neumann_left(room3)
    if A3_cache == None:
        A3_cache = A
    
    b = build_rhs_neumann_left(room3, flux)

    solution = solve(A.tocsc(), b)
    room3[1:-1, 1:] = solution.reshape((ny, nx))

    # Reconstruct the interface boundary
    room3[1:-1, 0] = room3[1:-1, 1] - dx * flux

    return room3

def solve_room2(room2):
    global A2_cache

    ny = room2.shape[0] - 2
    nx = room2.shape[1] - 2

    A = A2_cache if A2_cache != None else build_internal_matrix(room2,ny,nx)
    if A2_cache == None:
        A2_cache = A

    b = build_rhs_dirichlet(
        room2,
    )

    return solve_room(room2, b, A)

def solve_room1(room1, flux, nx, ny, dx):
    global A1_cache

    A = A1_cache if A1_cache != None else build_matrix_neumann_right(room1)
    if A1_cache == None:
        A1_cache = A
    
    b = build_rhs_neumann_right(room1, flux)

    solution = solve(A.tocsc(), b)
    room1[1:-1, :-1] = solution.reshape((ny, nx))

    # Reconstruct the interface boundary
    room1[1:-1, -1] = room1[1:-1, -2] + dx * flux

    return room1

def solve_room4(room4, flux, nx, ny, dx):
    global A4_cache

    A = A4_cache if A4_cache != None else build_matrix_neumann_left(room4)
    if A4_cache == None:
        A4_cache = A
    
    b = build_rhs_neumann_left(room4, flux)

    solution = solve(A.tocsc(),b)
    room4[1:-1,1:] = solution.reshape((ny,nx))
    room4[1:-1,0] = room4[1:-1,1]-dx*flux

    return room4
