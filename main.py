
### Placeholder import
# TODO
# setup init file for these functions
from modules import *
#from modules.geometry import create_room1, create_room2, create_room3, create_room4, floorplan_main, floorplan_addition
#from modules.MPI import send_npdata, recv_npdata, get_rank
#from modules.dn_MPI import dirichlet_neumann
#from modules.plot import plot_temperature
#import numpy as np
#from modules.constants import *

#DX = 1 / 3
#OMEGA = 0.8 
#N_ITERATIONS = 10
# TODO If Animate is not set to True, then there's no need to waste memory storing all the room states
# for the iterations. Only the first frame and last frame are needed.
#ANIMATE = True
#CROP = False
#INCLUDE_ROOM4 = False

def main():
    rank = get_rank()

    total_rooms = 3 if not INCLUDE_ROOM4 else 4
    if rank >= total_rooms:
        return
    
    print(f"DEBUG: rank={rank}", flush=True)
    if rank == 0:
        room = create_room1(DX)
    if rank == 1:
        room = create_room2(DX, include_room4=INCLUDE_ROOM4)
    if rank == 2:
        room = create_room3(DX)
    if INCLUDE_ROOM4 and rank == 3:
        room = create_room4(DX)

    solution = dirichlet_neumann(
        room,
        dx = DX,
        rank = rank,
        iterations = N_ITERATIONS,
        omega = OMEGA,
        include_room4=INCLUDE_ROOM4
        )
    if rank == 0:
        
        room2 = create_room2(DX, include_room4=INCLUDE_ROOM4)
        room3 = create_room3(DX)
        data2 = np.empty(
            (solution.shape[0], *room2.shape),
            dtype=float
        )
        data3 = np.empty(
            (solution.shape[0], *room3.shape),
            dtype=float
        )
                

        recv_npdata(data2, 1)
        recv_npdata(data3, 2)


        if INCLUDE_ROOM4:
            room4=create_room4(DX)
            data4=np.empty((solution.shape[0], *room4.shape), dtype=float)
            recv_npdata(data4,3)
            data=[[solution[i], data2[i], data3[i], data4[i]] for i in range(solution.shape[0])]
            floorplan_builder = floorplan_addition
        else:
            data = [[solution[i],data2[i],data3[i]] for i in range(solution.shape[0])]
            floorplan_builder=floorplan_main

        if CROP:
            data = [[room[1:-1,1:-1] for room in rooms] for rooms in data]
        if not ANIMATE:
            data = data[1:]
        plot_temperature(data, floorplan_builder=floorplan_builder, show_animation=ANIMATE)
        

    if rank == 1:
        send_npdata(solution,0)
        
    if rank == 2:
        send_npdata(solution,0)

    if rank == 3:
        send_npdata(solution ,0)
    
    


if __name__ == "__main__":
    main()