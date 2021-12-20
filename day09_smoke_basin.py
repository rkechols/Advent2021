import os
from bisect import insort
from typing import Tuple

import numpy as np

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input09.txt")

NEIGHBOR_SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
RIDGE_NUMBER = 9
HOW_MANY_BIGGEST = 3


def get_basin_size(grid: np.ndarray, low_point: Tuple[int, int]) -> int:
    in_basin = np.zeros_like(grid, dtype=bool)
    in_basin[low_point] = True
    neighbors = set()
    for i_shift, j_shift in NEIGHBOR_SHIFTS:
        new_i = low_point[0] + i_shift
        new_j = low_point[1] + j_shift
        if new_i < 0 or new_i >= grid.shape[0] or new_j < 0 or new_j >= grid.shape[1]:
            continue  # out-of-bounds
        if grid[new_i, new_j] != RIDGE_NUMBER:
            neighbors.add((new_i, new_j))
    while len(neighbors) > 0:
        next_neighbors = set()
        for i, j in neighbors:
            in_basin[i, j] = True
            for i_shift, j_shift in NEIGHBOR_SHIFTS:
                new_i = i + i_shift
                new_j = j + j_shift
                if new_i < 0 or new_i >= grid.shape[0] or new_j < 0 or new_j >= grid.shape[1]:
                    continue  # out-of-bounds
                if grid[new_i, new_j] != RIDGE_NUMBER and not in_basin[new_i, new_j]:
                    next_neighbors.add((new_i, new_j))
        neighbors = next_neighbors
    return in_basin.sum()


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
            lines.append(list(line))
    n_lines = len(lines)
    grid_ = np.empty((n_lines, line_len), dtype=int)
    for i_, line in enumerate(lines):
        for j_, num_char in enumerate(line):
            grid_[i_, j_] = int(num_char)
    # part 1
    risk_level = 0
    low_points = set()
    for i_ in range(n_lines):
        for j_ in range(line_len):
            # check if this point is the lowest of its neighbors
            this_val = grid_[i_, j_]
            for i_shift_, j_shift_ in NEIGHBOR_SHIFTS:
                new_i_ = i_ + i_shift_
                new_j_ = j_ + j_shift_
                if new_i_ < 0 or new_i_ >= n_lines or new_j_ < 0 or new_j_ >= line_len:
                    continue  # out-of-bounds
                if grid_[new_i_, new_j_] <= this_val:
                    break
            else:  # never hit break; all neighbors are > this_val
                low_points.add((i_, j_))
                risk_level += 1 + this_val
    print(f"TOTAL risk level: {risk_level}")
    # part 2
    biggest = list()
    for low_point_ in low_points:
        basin_size = get_basin_size(grid_, low_point_)
        insort(biggest, basin_size)
        if len(biggest) > HOW_MANY_BIGGEST:
            del biggest[0]  # get rid of the smallest
    assert len(biggest) == HOW_MANY_BIGGEST, "didn't get the right number of basins?"
    prod = 1
    for x in biggest:
        prod *= x
    print(f"PRODUCT of sizes of {HOW_MANY_BIGGEST} biggest basins: {prod}")
