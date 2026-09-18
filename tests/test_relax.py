
import sys
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from modules.dn_MPI import relax

def test_relax_identity():
    u = np.random.rand(5, 5)
    assert np.allclose(relax(u, u, omega=0.8), u)

def test_relax_half():
    u_new = np.ones((4, 4))
    u_old = np.zeros((4, 4))
    result = relax(u_new, u_old, 0.5)
    assert np.allclose(result, 0.5)
