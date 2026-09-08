
#solve Ω2 with Dirichlet
#        ↓
#solve Ω1 and Ω3 with Neumann
#        ↓
#relax
#        ↓
#repeat

def dirichlet_neumann_iteration(
    u1, u2, u3, room1, room2, room3, omega
):
    ...

def relax(u_new, u_old, omega):
    return omega * u_new + (1 - omega) * u_old