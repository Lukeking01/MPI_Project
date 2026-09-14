
### Placeholder import
# TODO
# setup init file for these functions
from modules.geometry import create_room1, create_room2, create_room3, floorplan_main
from modules.MPI import send_npdata, recv_npdata, get_rank
from modules.dn_MPI import dirichlet_neumann
from modules.plot import plot_temperature
import numpy as np


DX = 1 / 80
OMEGA = 0.8 
N_ITERATIONS = 10
ANIMATE = True
CROP = False

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
        rank = rank,
        iterations = N_ITERATIONS,
        omega = OMEGA
        )
    if rank == 0:
        
        room2 = create_room2(DX)
        room3 = create_room3(DX)
        data2 = np.empty(
            (N_ITERATIONS+1, *room2.shape),
            dtype=float
        )
        data3 = np.empty(
            (N_ITERATIONS+1, *room3.shape),
            dtype=float
        )
                

        recv_npdata(data2, 1)
        recv_npdata(data3, 2)

        if CROP:
            data = [[solution[i][1:-1,1:-1],data2[i][1:-1,1:-1],data3[i][1:-1,1:-1]] for i in range(N_ITERATIONS+1)]
        else:
            data = [[solution[i],data2[i],data3[i]] for i in range(N_ITERATIONS+1)]
        plot_temperature(data, floorplan_builder=floorplan_main, show_animation=ANIMATE)
        
    if rank == 1:
        send_npdata(solution,0)
        
    if rank == 2:
        send_npdata(solution,0)
    
    


if __name__ == "__main__":
    main()