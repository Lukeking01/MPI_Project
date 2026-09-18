import sys
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pytest
from modules.matrix import (
    build_A,
    build_rhs
)

def make_room(ny=5, nx=5, fill=0.0):
    """Helper: room of shape (ny+2, nx+2)."""
    return np.full((ny + 2, nx + 2), fill, dtype=float)

def test_internal_matrix_shape_and_stencil():
    A = build_A(3, 4)
    assert A.shape == (12, 12)
    # centre of first interior point should be -4
    assert A[0, 0] == -4
    # right neighbour
    assert A[0, 1] == 1

#
# THE FOLLOWING TESTS WERE FROM AN OUTDATED VERSION OF TESTING THE RHS FUNCTIONS
# They have not been updated.
#

# def test_rhs_dirichlet_moves_boundary_values():
#     room = make_room(2, 2, fill=0.0)
#     room[0, 1] = 10.0          # bottom
#     room[1, 0] = 20.0          # left
#     b = build_rhs_dirichlet(room)
#     # first interior point (j=0,i=0) feels bottom and left
#     assert b[0] == pytest.approx(-30.0)

# def test_neumann_right_changes_diagonal():
#     room = make_room(3, 3)
#     A = build_matrix_neumann_right(room)
#     # last column of each row should have -3 on diagonal
#     nx = 3
#     for j in range(3):
#         p = j * nx + (nx - 1)
#         assert A[p, p] == -3

# def test_neumann_left_changes_diagonal():
#     room = make_room(3, 3)
#     A = build_matrix_neumann_left(room)
#     nx = 3
#     for j in range(3):
#         p = j * nx
#         assert A[p, p] == -3