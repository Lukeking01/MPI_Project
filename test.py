

from modules.matrix import build_internal_matrix, build_matrix_neumann_right, build_matrix_neumann_left, build_rhs_dirichlet, build_rhs_neumann_left, build_rhs_neumann_right
from modules.geometry import create_room1, create_room2, create_room3, create_room4, get_interfaces
from modules.MPI import get_rank
from modules.dn_MPI import dirichlet_neumann
import numpy as np

rank = get_rank()

n=5

if rank == 0:
    room = create_room1(n)
if rank == 1:
    room = create_room2(n)
if rank == 2:
    room = create_room3(n)

if rank == 0:
    A = build_matrix_neumann_right(room)
if rank == 1:
    A = build_internal_matrix(room,2*n,n)
if rank == 2:
    A = build_matrix_neumann_left(room)

print(f"rank {rank}: {A.toarray()}")