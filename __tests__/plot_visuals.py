import sys
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from modules import plot_temperature
from modules.geometry import floorplan_main

### TEST NAMES AND ORDER

TEST_NAMES = {
    "TEST_STATIC_SQUARE": 1,
    "TEST_ANIMATE_SQUARE": 2,
    "TEST_BUILD_L_FLOORPLAN": 10,
    "TEST_BUILD_L_FLOORPLAN_OCEAN": 11,
}

### TEST FLOORPLAN BUILDERS

def get_L_room_frame(n):
    # Builds a series of three rooms for the L_FLOORPLAN tests.
    room_1 = np.random.normal(loc=18, scale=1.5, size=(n, n))  # Cool room (~18°C)
    room_2 = np.random.normal(loc=26, scale=1.0, size=(2*n, n))  # Warm room (~22°C)
    room_3 = np.random.normal(loc=33, scale=2.0, size=(n, n))  # Hot room (~26°C)

    return [room_1, room_2, room_3]

def L_floorplan_builder(rooms_frame):
    # Expects a single frame of "rooms" to be a list of 3 rooms.
    [room_1, room_2, room_3] = rooms_frame
    empty_space = np.full(room_1.shape, fill_value=np.nan)

    floorplan = np.hstack([
        np.block([[empty_space], [room_1]]),
        room_2,
        np.block([[room_3], [empty_space]])
    ])

    return floorplan

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

                plot_temperature(
                    frames,
                    main_title="TEST_STATIC_SQUARE", show_animation=False,
                )
            case 2:
                # Show a square dummy matrix with random data. Static starting/ending frames.
                frames = [create_dummy_array(n) for n in [50, 30, 20, 15, 12, 10]]

                plot_temperature(
                    frames, 
                    main_title="TEST_ANIMATE_SQUARE", show_animation=True,
                )
            case 10:
                # Shows an animated L-shaped floorplan.
                n = 10
                frames = [get_L_room_frame(n) for _ in range(5)]

                plot_temperature(
                    frames, floorplan_builder=L_floorplan_builder,
                    main_title="TEST_BUILD_L_FLOORPLAN", show_animation=True,
                )
            case 11:
                # Shows a floorplan with localised regions of data, but in the "Ocean" color scheme.
                n = 10
                frames = [get_L_room_frame(n) for _ in range(5)]

                plot_temperature(
                    frames, floorplan_builder=L_floorplan_builder,
                    main_title="TEST_BUILD_L_FLOORPLAN_OCEAN", show_animation=True, cmap="ocean",
                )

# Run the following tests:
tests = [
    TEST_NAMES["TEST_STATIC_SQUARE"],
    TEST_NAMES["TEST_ANIMATE_SQUARE"],
    TEST_NAMES["TEST_BUILD_L_FLOORPLAN"],
    TEST_NAMES["TEST_BUILD_L_FLOORPLAN_OCEAN"],
]
test_runner(tests=tests)
