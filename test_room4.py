from modules.geometry import create_room2, create_room4, exchange_neumann, exchange_dirichlet
from modules.MPI import get_rank

N = 8

rank = get_rank()

if rank == 1:
    U2 = create_room2(N, include_room4=True)
    exchange_dirichlet(U2, N, with_room4=True)
elif rank == 3:
    U4 = create_room4(N)
    exchange_dirichlet(U4, N, with_room4=True)
