from mpi4py import MPI

""" Get a communicator:
    The most common communicator is the
    one that connects all available processes
    which is called COMM_WORLD.
    Clone the communicator to avoid interference
    with other libraries or applications
"""
# Main project communictaor which can connect to all available processes.
# Clone the communicator to avoid interfering with other libraries.
comm = MPI.Comm.Clone( MPI.COMM_WORLD )

def get_rank():
    """
    Returns the rank of the current executing thread. This should be
    a number from 0 to the max number of threads minus one.
    """
    return comm.Get_rank()

def send_npdata(data, dest, tag = None):
    """
    Wrapper function which handles sending an np array.
    """
    comm.Send([data, MPI.DOUBLE], dest=dest, tag=tag)

def recv_npdata(data, dest, tag = None):
    """
    Wrapper function which handles receiving an np array.
    """
    comm.Recv([data, MPI.DOUBLE], dest=dest, tag=tag)
