

from scipy.linalg import solve

def solve_dirichlet(A, b):
    return solve(A, b)

def solve_neumann(A, b):
    return solve(A, b)