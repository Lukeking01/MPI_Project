
#solve Ω2 with Dirichlet
#        ↓
#solve Ω1 and Ω3 with Neumann
#        ↓
#relax
#        ↓
#repeat
import room_solver 

def dirichlet_neumann_iteration(
    u1, u2, u3, room1, room2, room3, omega
):
    """
    Perform the Dirichlet-Neumann iteration.

    room1, room2, room3:
        Information needed to solve each room.
        These variables might be deprecated in the future, as the room information is already contained in the temperature vectors.

    u1, u2, u3:
        Initial temperature vectors for the three rooms.

    omega:
        Relaxation parameter.
    """
    # 1. Solve Ω2 with Dirichlet conditions
    u2_new = room_solver.solve_dirichlet(
        room2,
        u1,
        u3
    )
    # 2. Solve Ω1 and Ω3 with Neumann conditions
    u1_new = room_solver.solve_neumann(
        room1,
        u2_new
    )
    u3_new = room_solver.solve_neumann(
        room3,
        u2_new
    )
    # 3. Relaxation
    u1 = relax(u1_new, u1, omega)
    u2 = relax(u2_new, u2, omega)
    u3 = relax(u3_new, u3, omega)

    return u1, u2, u3

def relax(u_new, u_old, omega):
    """
        Apply relaxation:
        u_new <- omega * u_new + (1 - omega) * u_old
    """
    return omega * u_new + (1 - omega) * u_old