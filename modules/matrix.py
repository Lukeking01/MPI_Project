
"""
Finite-difference matrices and right-hand sides for the heat equation.

This module builds the discrete Laplace operator on a uniform Cartesian
grid for both pure Dirichlet problems and mixed Dirichlet-Neumann
problems that arise in the Dirichlet-Neumann domain-decomposition
scheme.
"""

from scipy.sparse import lil_matrix
import numpy as np
from modules.constants import *

def build_A(nx, ny, neumann_sides=None):
    """
    Build the finite-difference matrix for nx * ny unknowns.

    Neumann boundaries use a first-order one-sided derivative
    together with a one-sided second derivative.
    """

    if neumann_sides is None:
        neumann_sides = set()
    else:
        neumann_sides = set(neumann_sides)

    N = nx * ny
    A = lil_matrix((N, N))

    def idx(i, j):
        return j * nx + i

    # ------------------------------------------------
    # Standard stencil
    # ------------------------------------------------

    for j in range(ny):
        for i in range(nx):

            row = idx(i, j)

            A[row, row] = -4

            if i > 0:
                A[row, idx(i - 1, j)] = 1

            if i < nx - 1:
                A[row, idx(i + 1, j)] = 1

            if j > 0:
                A[row, idx(i, j - 1)] = 1

            if j < ny - 1:
                A[row, idx(i, j + 1)] = 1

    # ------------------------------------------------
    # Neumann boundaries
    # ------------------------------------------------

    if "left" in neumann_sides:
        for j in range(ny):
            row = idx(0, j)

            A[row, row] = -3

            # Remove immediate inward neighbour
            A[row, idx(1, j)] = 0

            # Connect to second point inward
            if nx > 2:
                A[row, idx(2, j)] = 1

    if "right" in neumann_sides:
        for j in range(ny):
            row = idx(nx - 1, j)

            A[row, row] = -3

            # Remove immediate inward neighbour
            A[row, idx(nx - 2, j)] = 0

            # Connect to second point inward
            if nx > 2:
                A[row, idx(nx - 3, j)] = 1

    if "bottom" in neumann_sides:
        for i in range(nx):
            row = idx(i, 0)

            A[row, row] = -3
            A[row, idx(i, 1)] = 0

            if ny > 2:
                A[row, idx(i, 2)] = 1

    if "top" in neumann_sides:
        for i in range(nx):
            row = idx(i, ny - 1)

            A[row, row] = -3
            A[row, idx(i, ny - 2)] = 0

            if ny > 2:
                A[row, idx(i, ny - 3)] = 1

    return A.tocsr()

def build_A(nx, ny, neumann_sides=None):
    """
    Build the finite-difference matrix for nx * ny unknowns.

    Neumann boundaries use a first-order one-sided derivative
    together with a one-sided second derivative.
    """

    if neumann_sides is None:
        neumann_sides = set()
    else:
        neumann_sides = set(neumann_sides)

    N = nx * ny
    A = lil_matrix((N, N))

    def idx(i, j):
        return j * nx + i

    # ------------------------------------------------
    # Standard stencil
    # ------------------------------------------------

    for j in range(ny):
        for i in range(nx):

            row = idx(i, j)

            A[row, row] = -4

            if i > 0:
                A[row, idx(i - 1, j)] = 1

            if i < nx - 1:
                A[row, idx(i + 1, j)] = 1

            if j > 0:
                A[row, idx(i, j - 1)] = 1

            if j < ny - 1:
                A[row, idx(i, j + 1)] = 1

    # ------------------------------------------------
    # Neumann boundaries
    # ------------------------------------------------

    if "left" in neumann_sides:
        for j in range(ny):
            row = idx(0, j)

            A[row, row] = -3

            # Remove immediate inward neighbour
            A[row, idx(1, j)] = 0

            # Connect to second point inward
            if nx > 2:
                A[row, idx(2, j)] = 1

    if "right" in neumann_sides:
        for j in range(ny):
            row = idx(nx - 1, j)

            A[row, row] = -3

            # Remove immediate inward neighbour
            A[row, idx(nx - 2, j)] = 0

            # Connect to second point inward
            if nx > 2:
                A[row, idx(nx - 3, j)] = 1

    if "bottom" in neumann_sides:
        for i in range(nx):
            row = idx(i, 0)

            A[row, row] = -3
            A[row, idx(i, 1)] = 0

            if ny > 2:
                A[row, idx(i, 2)] = 1

    if "top" in neumann_sides:
        for i in range(nx):
            row = idx(i, ny - 1)

            A[row, row] = -3
            A[row, idx(i, ny - 2)] = 0

            if ny > 2:
                A[row, idx(i, ny - 3)] = 1

    return A.tocsr()

def build_A(nx, ny, neumann_sides=None):

    if neumann_sides is None:
        neumann_sides = set()
    else:
        neumann_sides = set(neumann_sides)

    N = nx * ny
    A = lil_matrix((N, N))

    def idx(i, j):
        return j * nx + i

    # ------------------------------------------------
    # Standard interior stencil
    # ------------------------------------------------

    for j in range(ny):
        for i in range(nx):

            row = idx(i, j)

            A[row, row] = -4

            if i > 0:
                A[row, idx(i - 1, j)] = 1

            if i < nx - 1:
                A[row, idx(i + 1, j)] = 1

            if j > 0:
                A[row, idx(i, j - 1)] = 1

            if j < ny - 1:
                A[row, idx(i, j + 1)] = 1

    # ------------------------------------------------
    # Left Neumann
    # ------------------------------------------------

    if "left" in neumann_sides:

        for j in range(ny):

            row = idx(0, j)

            A[row, row] = -3

            # Remove immediate neighbour
            A[row, idx(1, j)] = 0

            # Add second point inward
            A[row, idx(2, j)] = 1

    # ------------------------------------------------
    # Right Neumann
    # ------------------------------------------------

    if "right" in neumann_sides:

        for j in range(ny):

            row = idx(nx - 1, j)

            A[row, row] = -3

            # Remove immediate neighbour
            A[row, idx(nx - 2, j)] = 0

            # Add second point inward
            A[row, idx(nx - 3, j)] = 1

    # ------------------------------------------------
    # Bottom Neumann
    # ------------------------------------------------

    if "bottom" in neumann_sides:

        for i in range(nx):

            row = idx(i, 0)

            A[row, row] = -3

            A[row, idx(i, 1)] = 0

            A[row, idx(i, 2)] = 1

    # ------------------------------------------------
    # Top Neumann
    # ------------------------------------------------

    if "top" in neumann_sides:

        for i in range(nx):

            row = idx(i, ny - 1)

            A[row, row] = -3

            A[row, idx(i, ny - 2)] = 0

            A[row, idx(i, ny - 3)] = 1

    return A.tocsr()

def build_rhs(room, nx, ny, neumann_sides=None, flux=None):

    if neumann_sides is None:
        neumann_sides = set()
    else:
        neumann_sides = set(neumann_sides)

    if flux is None:
        flux = {}

    b = np.zeros(nx * ny)

    def idx(i, j):
        return j * nx + i

    # --------------------------------------------------
    # Dirichlet contributions
    # --------------------------------------------------

    for j in range(ny):
        for i in range(nx):

            p = idx(i, j)

            # bottom
            if j == 0 and "bottom" not in neumann_sides:
                b[p] -= room[0, i + 1]

            # top
            if j == ny - 1 and "top" not in neumann_sides:
                b[p] -= room[-1, i + 1]

            # left
            if i == 0 and "left" not in neumann_sides:
                b[p] -= room[j + 1, 0]

            # right
            if i == nx - 1 and "right" not in neumann_sides:
                b[p] -= room[j + 1, -1]

    # --------------------------------------------------
    # Neumann contributions
    # --------------------------------------------------

    if "left" in neumann_sides:
        q = np.asarray(flux.get("left", np.zeros(ny)))

        for j in range(ny):
            b[idx(0, j)] -= 2 * DX * q[j]

    if "right" in neumann_sides:
        q = np.asarray(flux.get("right", np.zeros(ny)))

        for j in range(ny):
            b[idx(nx - 1, j)] -= 2 * DX * q[j]

    if "bottom" in neumann_sides:
        q = np.asarray(flux.get("bottom", np.zeros(nx)))

        for i in range(nx):
            b[idx(i, 0)] -= 2 * DX * q[i]

    if "top" in neumann_sides:
        q = np.asarray(flux.get("top", np.zeros(nx)))

        for i in range(nx):
            b[idx(i, ny - 1)] -= 2 * DX * q[i]

    return b
