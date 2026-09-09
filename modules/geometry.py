import numpy as np
### apartment layout

def create_room1(dx):
    x = int(1.0/dx) + 1
    y = int(1.0/dx) + 1

    U1 = np.zeros((y, x))

    U1[0, :] = 15
    U1[-1, :] = 15
    U1[:, 0] = 40

    return U1

def create_room2(dx):
    x = int(1.0/dx) + 1
    y = int(2.0/dx) + 1

    U2 = np.zeros((y, x))

    middle = int(1.0/dx)

    U2[0, :] = 5
    U2[middle:, 0] = 15
    U2[-1, :] = 40
    U2[:middle + 1, -1] = 15

    return U2

def create_room3(dx):
    x = int(1.0/dx) + 1
    y = int(1.0/dx) + 1

    U3 = np.zeros((y, x))

    U3[0, :] = 15
    U3[:, -1] = 40
    U3[-1, :] = 15

    return U3

def get_interfaces(U1, U2, U3, dx):
    middle = int(1.0/dx)

    #Dirichlet boundary conditions
    U2[:middle + 1, 0] = U1[:, -1]
    U2[middle:, -1] = U3[:, 0]

    #Neumann boundary conditions
    n1 = (U2[:middle + 1, 1] - U2[:middle + 1, 0]) / dx
    n2 = (U2[middle:, -1] - U2[middle:, -2]) / dx

    return U2, n1, n2
