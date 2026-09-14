

from scipy.sparse.linalg import spsolve as solve

def room_solver(A, b):
    u = solve(A, b)
    return u