import os
from copy import deepcopy

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input15.txt")


if __name__ == "__main__":
    lines = list()
    cols = None
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            line = line_.strip()
            if cols is None:
                cols = len(line)
            else:
                assert len(line) == cols, "line lengths not consistent?"
            lines.append(line)
    rows = len(lines)
    costs = [[int(num_char) for num_char in line] for line in lines]
    # iterate
    grid = [[None] * cols for _ in range(rows)]
    grid[0][0] = 0
    while True:
        changed = False
        new_grid = deepcopy(grid)
        for i_ in range(rows):
            for j_ in range(cols):
                # do any of the neighbors of this spot get us a better score?
                options = set()
                no_movement = grid[i_][j_]
                if no_movement is not None:
                    options.add(no_movement)
                for i_shift, j_shift in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    new_i = i_ + i_shift
                    if new_i < 0 or new_i >= rows:
                        continue
                    new_j = j_ + j_shift
                    if new_j < 0 or new_j >= cols:
                        continue
                    to_add = grid[new_i][new_j]
                    if to_add is not None:
                        options.add(costs[i_][j_] + to_add)
                if len(options) == 0:
                    continue
                best = min(options)
                new_grid[i_][j_] = best
        if new_grid == grid:
            break  # no change
        grid = new_grid
    print(f"BEST cost: {grid[-1][-1]}")
