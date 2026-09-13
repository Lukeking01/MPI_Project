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

    :returns int: Integer representing the rank of the current thread.
    """
    return comm.Get_rank()

def send_npdata(data, dest: int, tag: int = 0):
    """
    Wrapper function which handles sending an np array.
    
    :param data:
    :param source: The rank of the thread sending the data.
    :param tag: Integer tag sent with the data.
    :returns None:
    """
    comm.Send([data, MPI.DOUBLE], dest=dest, tag=tag)

def recv_npdata(data, source: int, tag: int = None):
    """
    Wrapper function which handles receiving an np array.

    :param data:
    :param source: The rank of the thread sending the data.
    :param tag: Integer tag sent with the data.
    :returns None:
    """
    recv_kwargs = { "source": source }
    if tag is not None:
        recv_kwargs["tag"] = tag
    
    comm.Recv([data, MPI.DOUBLE], **recv_kwargs)
