
import sys
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from modules.geometry import create_room1, create_room2, create_room3, create_room4

def test_room_shapes_dx_0_05():
    n = 20
    assert create_room1(n).shape == (20, 20)
    assert create_room2(n).shape == (40, 20)
    assert create_room3(n).shape == (20, 20)
    assert create_room4(n).shape == (10, 10)

def test_room1_boundary_values():
    U = create_room1(10)
    assert np.all(U[0, 1:-1] == 15)
    assert np.all(U[-1, 1:-1] == 15)
    assert np.all(U[1:-1, 0] == 40)
