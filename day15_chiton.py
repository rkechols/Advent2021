import os
from typing import List

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input15.txt")

SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
GRID_MULTIPLICATION = 5
NUMBER_LIMIT = 9


def solve(costs: List[List[int]]) -> int:
    rows = len(costs)
    cols = len(costs[0])
    grid = [[None] * cols for _ in range(rows)]
    grid[0][0] = 0
    previously_changed = {(0, 0)}
    while True:
        # put all neighbors of ones that have changed into a set of ones to check
        to_check = set()
        for i, j in previously_changed:
            for i_shift, j_shift in SHIFTS:
                new_i = i + i_shift
                if new_i < 0 or new_i >= rows:
                    continue
                new_j = j + j_shift
                if new_j < 0 or new_j >= cols:
                    continue
                to_check.add((new_i, new_j))
        # check each one that may need to change, record if it does
        changed = set()
        for i, j in to_check:
            # do any of the neighbors of this spot get us a better score?
            options = set()
            no_movement = grid[i][j]
            if no_movement is not None:
                options.add(no_movement)
            for i_shift, j_shift in SHIFTS:
                new_i = i + i_shift
                if new_i < 0 or new_i >= rows:
                    continue
                new_j = j + j_shift
                if new_j < 0 or new_j >= cols:
                    continue
                to_add = grid[new_i][new_j]
                if to_add is not None:
                    options.add(costs[i][j] + to_add)
            if len(options) == 0:
                continue
            best = min(options)
            if best != grid[i][j]:
                changed.add((i, j))
                grid[i][j] = best
        if len(changed) == 0:
            break  # no change
        previously_changed = changed
    return grid[-1][-1]


if __name__ == "__main__":
    lines = list()
    line_len = None
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            line = line_.strip()
            if line_len is None:
                line_len = len(line)
            else:
                assert len(line) == line_len, "line lengths not consistent?"
            lines.append(line)
    n_lines = len(lines)
    costs_ = [[int(num_char) for num_char in line] for line in lines]
    # part 1: normal size map
    best_cost = solve(costs_)
    print(f"BEST cost: {best_cost}")
    print("------")
    # part 2: extended map
    costs_big = list()
    for row_section in range(GRID_MULTIPLICATION):
        for row in costs_:
            new_row = list()
            for col_section in range(GRID_MULTIPLICATION):
                for val in row:
                    full_val = val + row_section + col_section
                    while full_val > NUMBER_LIMIT:
                        full_val -= NUMBER_LIMIT
                    new_row.append(full_val)
            costs_big.append(new_row)
    best_cost = solve(costs_big)
    print(f"BEST cost: {best_cost}")
