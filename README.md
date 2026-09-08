# MPI_Project
Project in solving the heat equation using MPI in the course NUMN21


main.py -	Run the whole project
geometry.py -	Define the three rooms and their interfaces
matrix.py -	Construct the finite-difference matrices
room_solver.py -	Solve one room with given boundary conditions
dn.py -	Implement the dirichlet neumann iteration and relaxation
mpi.py -	MPI ranks and communication between rooms
plot.py -	Plot the final temperature distribution
