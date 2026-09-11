
import numpy as np
def build_internal_matrix(room):
    """
    Build the finite-difference matrix for the interior unknowns.
    """
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
    Build RHS for a room with Dirichlet boundary conditions.
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
    Build matrix for a room with a Neumann condition
    on the right boundary.

    Uses:
        u_ghost = u_interior - dx * flux

    which changes -4 to -3 for points adjacent
    to the Neumann boundary.
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
    Build RHS for:

        - Dirichlet on left, bottom and top
        - Neumann on right

    flux[j] contains one flux value for each
    interior row.
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
                b[p] += dx * flux[j]

    return b

def build_matrix_neumann_left(room):
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
    Left boundary = Neumann
    Right boundary = heater
    Top/bottom = normal walls
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

