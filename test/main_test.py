import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import main as main

class MainTest():

    def test_grid_init():
        grid, subgrids = main.MainClass.grid_init()

        assert grid.size == 10000, f"Total grid size is {grid.size}."
        assert len(grid) == 100, f"Total grid row length is {len(grid)}."
        assert len(subgrids) == 20, f"Total subgrid length is {len(subgrids)}."
        assert all(len(row) == 100 for row in grid), f"Total grid column length is {(len(row) for row in grid)}."
        assert all(len(row) == 20 for row in subgrids), f"Subgrid rows have a length of {(len(row) for row in subgrids)}."
        

    test_grid_init()
    print("grid_init function passed all tests.")