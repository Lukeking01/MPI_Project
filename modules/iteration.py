
# solve Ω2 with Dirichlet
#        ↓
# solve Ω1 and Ω3 and Ω4 with Neumann
#        ↓
# relax
#        ↓
# repeat

from .room_solver import room_solver as solve
from .matrix import build_rhs, build_A
from .constants import *

# Save the A matrices between iterations
A1_cache = None
A2_cache = None
A3_cache = None
A4_cache = None

### Solvers ###
# 1. Build the LHS sparse matrix A if not already built
# 2. Build the RHS matrix b
# 3. Run the sparse solver
# 4. Return updated room state with result

def solve_room1(room1, flux):
    global A1_cache

    nx, ny = N-1, N-2
    
    A = A1_cache if A1_cache != None else build_A(nx, ny, ["right"])
    if A1_cache == None:
        A1_cache = A
    
    b = build_rhs(room1, nx, ny, ["right"], flux)

    solution = solve(A, b)
    room1[1:-1, 1:] = solution.reshape((ny, nx))

    return room1


def solve_room2(room2):
    global A2_cache

    ny = room2.shape[0] - 2
    nx = room2.shape[1] - 2

    A = A2_cache if A2_cache != None else build_A(nx,ny)
    if A2_cache == None:
        A2_cache = A

    b = build_rhs(room2, nx, ny)

    solution = solve(A, b)
    room2[1:-1, 1:-1] = solution.reshape((ny, nx))

    return room2


def solve_room3(room3, flux):
    global A3_cache
    
    nx, ny = N-1, N-2

    A = A3_cache if A3_cache != None else build_A(nx, ny, ["left"])
    if A3_cache == None:
        A3_cache = A
    
    b = build_rhs(room3, nx, ny, ["left"], flux)

    solution = solve(A, b)
    room3[1:-1, :-1] = solution.reshape((ny, nx))

    return room3


def solve_room4(room4, flux):
    global A4_cache

    nx, ny = int(N/2-1), int(N/2-2)

    A = A4_cache if A4_cache != None else build_A(nx, ny, ["left"])
    if A4_cache == None:
        A4_cache = A
    
    b = build_rhs(room4, nx, ny, ["left"], flux)

    solution = solve(A,b)
    room4[1:-1,:-1] = solution.reshape((ny, nx))

    return room4
