

from modules.matrix import build_internal_matrix, build_matrix_neumann_right, build_matrix_neumann_left, build_rhs_dirichlet, build_rhs_neumann_left, build_rhs_neumann_right, build_A
from modules.geometry import create_room1, create_room2, create_room3, create_room4, get_interfaces
from modules.MPI import get_rank
from modules.dn_MPI import dirichlet_neumann
from modules.dn_MPI import dn_iteration
import numpy as np

rank = get_rank()

n=3

if rank == 0:
    room = create_room1(n)
if rank == 1:
    room = create_room2(n,0)
if rank == 2:
    room = create_room3(n)
if rank == 3:
    room = create_room4(n)
print(f"before rank {rank}: \n{room}")
if rank == 0:
    A = build_A(n-1,n-2,["right"])
if rank == 1:
    A = build_A(n-2,2*n-2)
if rank == 2:
    A = build_A(n-1,n-2,["left"])
if rank == 3:
    A = build_A(int(n/2),int(n/2),["left"])


    
room = dn_iteration(room,n,rank)

print(f"rank {rank}: {room}")