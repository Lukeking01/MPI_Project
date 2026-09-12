"""
Mapping the file importing sequence

                    main.py
 
 ↓              ↓        ↓          ↓
 ↓              ↓     MPI.py ←  geometry.py   ←   iteration.py                  
 ↓              ↓                             ↙          ↓            
 ↓              ↓        
plot.py      dn.py                  room_solver.py      matrix.py         
                                               
"""

from .geometry import create_room1, create_room2, create_room3
from .MPI import send_npdata, recv_npdata, get_rank
from .dn import dirichlet_neumann
from .plot import plot_temperature