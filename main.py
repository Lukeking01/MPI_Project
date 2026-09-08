
from geometry import ...
from dirichlet_neumann import ...
from plot import ...

DX = 1 / 20
OMEGA = 0.8
N_ITERATIONS = 10

def main():
    rooms = create_rooms(DX)

    solution = run_dirichlet_neumann(
        rooms,
        omega=OMEGA,
        iterations=N_ITERATIONS
    )

    plot_temperature(solution)


if __name__ == "__main__":
    main()