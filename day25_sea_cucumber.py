import os
from copy import deepcopy
from itertools import count
from typing import List, Tuple

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input25.txt")

EAST = ">"
SOUTH = "v"
EMPTY = "."


def time_step(grid: List[List[str]]) -> Tuple[List[List[str]], bool]:
    n_rows = len(grid)
    n_cols = len(grid[0])
    changed = False
    # east/right
    new_grid = deepcopy(grid)
    for i in range(n_rows):
        for j in range(n_cols):
            if grid[i][j - 1] == EAST and grid[i][j] == EMPTY:
                changed = True
                new_grid[i][j - 1] = EMPTY
                new_grid[i][j] = EAST
    grid = new_grid
    # south/down
    new_grid = deepcopy(grid)
    for i in range(n_rows):
        for j in range(n_cols):
            if grid[i - 1][j] == SOUTH and grid[i][j] == EMPTY:
                changed = True
                new_grid[i - 1][j] = EMPTY
                new_grid[i][j] = SOUTH
    grid = new_grid
    # return final update
    return grid, changed


if __name__ == "__main__":
    grid_ = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            grid_.append(list(line_.strip()))
    # simulate
    for step in count(start=1):
        grid_, changed_ = time_step(grid_)
        if not changed_:
            print(f"STOPPED moving at step {step}")
            break
