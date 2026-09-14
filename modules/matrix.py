
"""
Finite-difference matrices and right-hand sides for the heat equation.

This module builds the discrete Laplace operator on a uniform Cartesian
grid for both pure Dirichlet problems and mixed Dirichlet-Neumann
problems that arise in the Dirichlet-Neumann domain-decomposition
scheme.
"""

import numpy as np
def build_internal_matrix(room):
    """
    Build the finite-difference matrix for the interior unknowns.

    The matrix corresponds to the standard five-point stencil

        u_{i-1,j} + u_{i+1,j} + u_{i,j-1} + u_{i,j+1} - 4 u_{i,j} = 0

    on the interior nodes only.  Boundary contributions are moved to the
    right-hand side by the companion RHS builders.

    Parameters
    ----------
    room : ndarray
        Temperature field of shape ``(ny+2, nx+2)`` that includes a one-cell
        layer of boundary values.  Only the shape is used; the values
        themselves are ignored.

    Returns
    -------
    ndarray
        Dense matrix of shape ``((nx*ny), (nx*ny))`` where
        ``nx = room.shape[1]-2`` and ``ny = room.shape[0]-2``.
    """"
    ny, nx = room.shape
    ny -= 2
    nx -= 2

    A = np.zeros((nx * ny, nx * ny))

    for j in range(ny):
        for i in range(nx):

            index = j * nx + i

            # Center
            A[index, index] = -4

            # Left
            if i > 0:
                A[index, index - 1] = 1

            # Right
            if i < nx - 1:
                A[index, index + 1] = 1

            # Top
            if j > 0:
                A[index, index - nx] = 1

            # Bottom
            if j < ny - 1:
                A[index, index + nx] = 1

    return A


def build_rhs_dirichlet(room):
    """
    Build the right-hand side for a pure Dirichlet problem.

    All four sides of the room are treated as Dirichlet boundaries.
    Their known values are moved to the right-hand side of the linear
    system that is formed with :func:`build_internal_matrix`.

    Parameters
    ----------
    room : ndarray
        Temperature field of shape ``(ny+2, nx+2)`` containing the
        current Dirichlet data on all four boundaries.

    Returns
    -------
    ndarray
        Vector of length ``nx*ny`` that forms the right-hand side of
        ``A u = b``.
    """
    ny, nx = room.shape
    ny -= 2
    nx -= 2
    
    b = np.zeros(nx * ny)

    for j in range(ny):
        for i in range(nx):

            p = j * nx + i

            # Bottom boundary
            if j == 0:
                b[p] -= room[0, i + 1]

            # Top boundary
            if j == ny - 1:
                b[p] -= room[ny + 1, i + 1]

            # Left boundary
            if i == 0:
                b[p] -= room[j + 1, 0]

            # Right boundary
            if i == nx - 1:
                b[p] -= room[j + 1, nx + 1]

    return b


def build_matrix_neumann_right(room):
    """
    Build the system matrix for a Neumann condition on the right boundary.

    Starting from the pure interior matrix, the diagonal entry of every
    node adjacent to the right boundary is changed from -4 to -3.  This
    corresponds to the second-order approximation

        u_ghost = u_interior - dx * flux

    that eliminates the fictitious exterior node.

    Parameters
    ----------
    room : ndarray
        Temperature field whose shape determines the grid size
        (``ny+2, nx+2``).

    Returns
    -------
    ndarray
        Modified dense matrix of shape ``((nx*ny), (nx*ny))``.
    """
    ny, nx = room.shape
    ny -= 2
    nx -= 2

    A = build_internal_matrix(room)

    for j in range(ny):

        # Last interior point in each row
        p = j * nx + (nx - 1)

        A[p, p] = -3

    return A


def build_rhs_neumann_right(room, flux):
    """
    Build the right-hand side for a Neumann condition on the right side.

    The left, bottom and top boundaries remain Dirichlet; the right
    boundary is Neumann.  The supplied flux values appear on the
    right-hand side multiplied by the mesh width ``dx``.

    Parameters
    ----------
    room : ndarray
        Temperature field of shape ``(ny+2, nx+2)`` containing the
        known Dirichlet data on the three non-Neumann sides.
    flux : ndarray
        One-dimensional array of length ``ny`` holding the Neumann flux
        at each interior row of the right boundary.

    Returns
    -------
    ndarray
        Vector of length ``nx*ny`` that forms the right-hand side of
        the linear system.
    """
    ny, nx = room.shape
    ny -= 2
    nx -= 2

    dx = 1 / (nx + 1)

    b = np.zeros(nx * ny)

    for j in range(ny):
        for i in range(nx):

            p = j * nx + i

            # Left heater
            if i == 0:
                b[p] -= room[j + 1, 0]

            # Bottom wall
            if j == 0:
                b[p] -= room[0, i + 1]

            # Top wall
            if j == ny - 1:
                b[p] -= room[ny + 1, i + 1]

            # Right Neumann boundary
            if i == nx - 1:
                b[p] -= dx * flux[j]

    return b

def build_matrix_neumann_left(room):
    """
    Build the system matrix for a Neumann condition on the left boundary.

    Analogous to :func:`build_matrix_neumann_right`, the diagonal entry of
    every node adjacent to the left boundary is changed from -4 to -3.

    Parameters
    ----------
    room : ndarray
        Temperature field whose shape determines the grid size
        (``ny+2, nx+2``).

    Returns
    -------
    ndarray
        Modified dense matrix of shape ``((nx*ny), (nx*ny))``.
    """
    ny, nx = room.shape
    ny -= 2
    nx -= 2
    A = build_internal_matrix(room)

    for j in range(ny):
        p = j * nx

        # Point next to left Neumann boundary
        A[p, p] = -3

    return A


def build_rhs_neumann_left(room, flux):
    """
    Build the right-hand side for a Neumann condition on the left side.

    The right, bottom and top boundaries remain Dirichlet; the left
    boundary is Neumann.  The supplied flux values appear on the
    right-hand side multiplied by the mesh width ``dx``.

    Parameters
    ----------
    room : ndarray
        Temperature field of shape ``(ny+2, nx+2)`` containing the
        known Dirichlet data on the three non-Neumann sides.
    flux : ndarray
        One-dimensional array of length ``ny`` holding the Neumann flux
        at each interior row of the left boundary.

    Returns
    -------
    ndarray
        Vector of length ``nx*ny`` that forms the right-hand side of
        the linear system.
    """
    ny, nx = room.shape
    ny -= 2
    nx -= 2
    dx = 1 / (nx + 1)
    b = np.zeros(nx * ny)

    for j in range(ny):
        for i in range(nx):

            p = j * nx + i

            # Right heater
            if i == nx - 1:
                b[p] -= room[j + 1, nx + 1]

            # Bottom wall
            if j == 0:
                b[p] -= room[0, i + 1]

            # Top wall
            if j == ny - 1:
                b[p] -= room[ny + 1, i + 1]

            # Left Neumann
            if i == 0:
                b[p] -= dx * flux[j]

    return b

