

from scipy.sparse.linalg import spsolve as solve

def room_solver(A, b):
    """
    Runs a sparse solver to get a solution to A @ u = b.

    :returns: Flattened new room state u
    """
    
    u = solve(A, b)
    return u