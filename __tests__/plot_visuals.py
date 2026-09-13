import sys
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from modules import plot_temperature

### TEST NAMES AND ORDER

TEST_NAMES = {
    "TEST_STATIC_SQUARE": 1,
    "TEST_ANIMATE_SQUARE": 2,
    "TEST_BUILD_FLOORPLAN": 10,
    "TEST_BUILD_FLOORPLAN_OCEAN": 11,
}

### HELPER FUNCS

def create_dummy_array(m: int, n: int = None):
    """
    Dummy function, simply creates a mock output of an m x n grid, with random temperature
    data in cells ranging from 20 to 80.
    """
    if not n:
        n = m
    
    return 15 + 20 * np.random.random((m, n))

### TEST RUNNER

def test_runner(tests: list[int]):
    """
    Runs all tests defined by the TEST_NAMES
    """
    
    for test_num in tests:
        match test_num:
            case 1:
                # Show a square dummy matrix with random data. Static starting/ending frames.
                frames = [create_dummy_array(n) for n in [50, 30, 20, 15, 12, 10]]

                plot_temperature(frames, show_animation=False)
            case 2:
                # Show a square dummy matrix with random data. Static starting/ending frames.
                frames = [create_dummy_array(n) for n in [50, 30, 20, 15, 12, 10]]

                plot_temperature(frames, show_animation=True)
            case 10:
                # Shows a floorplan with localised regions of data, but in the "Ocean" color scheme.
                n = 10
                empty_space = np.full((n, n), fill_value=np.nan)
                room_1 = np.random.normal(loc=18, scale=1.5, size=(n, n))  # Cool room (~18°C)
                room_2 = np.random.normal(loc=26, scale=1.0, size=(2*n, n))  # Warm room (~22°C)
                room_3 = np.random.normal(loc=33, scale=2.0, size=(n, n))  # Hot room (~26°C)

                floorplan = np.hstack([
                    np.block([[empty_space], [room_1]]),
                    room_2,
                    np.block([[room_3], [empty_space]])
                ])
                frames = [floorplan]

                plot_temperature(frames, show_animation=False)
            case 11:
                # Shows a floorplan with localised regions of data, but in the "Ocean" color scheme.
                n = 10
                empty_space = np.full((n, n), fill_value=np.nan)
                room_1 = np.random.normal(loc=18, scale=1.5, size=(n, n))  # Cool room (~18°C)
                room_2 = np.random.normal(loc=26, scale=1.0, size=(2*n, n))  # Warm room (~22°C)
                room_3 = np.random.normal(loc=33, scale=2.0, size=(n, n))  # Hot room (~26°C)

                floorplan = np.hstack([
                    np.block([[empty_space], [room_1]]),
                    room_2,
                    np.block([[room_3], [empty_space]])
                ])
                frames = [floorplan]

                plot_temperature(frames, show_animation=False, cmap="ocean")

# Run the following tests:
tests = [
    TEST_NAMES["TEST_STATIC_SQUARE"],
    TEST_NAMES["TEST_ANIMATE_SQUARE"],
    TEST_NAMES["TEST_BUILD_FLOORPLAN"],
    TEST_NAMES["TEST_BUILD_FLOORPLAN_OCEAN"],
]
test_runner(tests=tests)
