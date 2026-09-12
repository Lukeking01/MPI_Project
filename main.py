
### Placeholder import
# TODO
# setup init file for these functions
from modules import create_room1, create_room2, create_room3, send_npdata, rcv_npdata, get_rank, dirichlet_neumann, plot_temperature
import numpy as np


DX = 1 / 20
OMEGA = 0.8
N_ITERATIONS = 10

def main():
    rank = get_rank()
    
    if rank == 0:
        room = create_room1(DX)
    if rank == 1:
        room = create_room2(DX)
    if rank == 2:
        room = create_room3(DX)

    solution = dirichlet_neumann(
        room,
        dx = DX,
        rank = rank
        iterations = N_ITERATIONS,
        omega = OMEGA
    )
    if rank == 0:
        size2 = np.zeros(1,1,1)
        size3 = np.zeros(1,1,1)
        
        rcv_npdata(size2,1)
        rcv_npdata(size3,2)
        
        data2 = np.zeros(size2)
        data3 = np.zeros(size3)
        rcv_npdata(data2,1)
        rcv_npdata(data3,2)
        data = zip(solution,data2,data3)
        
    if rank == 1:
        send_npdata(solution.shape,0)
        send_npdata(solution,0)
        
    if rank == 2:
        send_npdata(solution.shape,0)
        send_npdata(solution,0)
    
    plot_temperature(data)


if __name__ == "__main__":
    main()