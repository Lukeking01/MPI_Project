

from scipy.linalg import solve

def room_solver(A, b):
    u = solve(A, b)
    return u