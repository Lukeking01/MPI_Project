
import sys
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from modules.geometry import create_room2
from modules.room_solver import solve_room2

def test_solve_room2_runs():
    room = create_room2(n=10)

    # just check that it returns an array of the same shape and does not blow up
    result = solve_room2(room.copy())
    assert result.shape == room.shape
    assert np.isfinite(result).all()
