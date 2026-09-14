from modules.matrix import build_internal_matrix, build_matrix_neumann_right, build_matrix_neumann_left, build_rhs_dirichlet, build_rhs_neumann_left, build_rhs_neumann_right
from modules.geometry import create_room1, create_room2, create_room3, create_room4, get_interfaces
from modules.MPI import get_rank
from modules.dn_MPI import dirichlet_neumann
import numpy as np

rank = get_rank()

dx=1/3
if rank == 0:
    room = create_room1(dx)
if rank == 1:
    room = create_room2(dx)
if rank == 2:
    room = create_room3(dx)

if rank == 0:
    matrix = build_matrix_neumann_right(room)
if rank == 1:
    matrix = build_matrix_neumann_left(room)
if rank == 2:
    matrix = build_internal_matrix(room)

flux = get_interfaces(room, dx)
if rank == 0:
    matrixb1 = build_rhs_neumann_right(room,flux)
if rank == 1:
    matrixb2 = build_rhs_dirichlet(room)
if rank == 2:
    matrixb3 = build_rhs_neumann_left(room,flux)

if rank == 0:
    print("room 1", matrixb1)
    print()
if rank == 1:
    print("room 2", matrixb2)
    print()
if rank == 2:
    print("room 3", matrixb3)
    print()

if rank == 0:
    solved1 = dirichlet_neumann(room, dx, rank)
    print("room1", solved1[-1])
if rank == 1:
    solved1 = dirichlet_neumann(room, dx, rank)
    print("room2", solved1[-1])
if rank == 2:
    solved1 = dirichlet_neumann(room, dx, rank)
    print("room3", solved1[-1])