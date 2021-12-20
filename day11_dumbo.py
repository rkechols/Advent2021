import os
from itertools import count

import numpy as np

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input11.txt")

N_STEPS = 100
FLASH_LEVEL = 10
RESET_LEVEL = 0

SHIFTS = [-1, 0, 1]


def timestep(grid: np.ndarray) -> int:
    is_flashing = np.zeros_like(grid, dtype=bool)
    grid += 1
    while True:
        # find which ones are flashing
        new_flashes = np.zeros_like(is_flashing)
        for i in range(is_flashing.shape[0]):
            for j in range(is_flashing.shape[1]):
                # if this one has enough energy, and we haven't already marked it, then mark it
                if grid[i, j] >= FLASH_LEVEL and not is_flashing[i, j]:
                    new_flashes[i, j] = True
        # end of the chain reaction?
        if new_flashes.sum() == 0:
            break
        # update master grid
        is_flashing += new_flashes
        # add energy to neighbors of flashing ones
        for i in range(new_flashes.shape[0]):
            for j in range(new_flashes.shape[1]):
                if new_flashes[i, j]:
                    for i_shift in SHIFTS:
                        new_i = i + i_shift
                        if new_i < 0 or new_i >= new_flashes.shape[0]:
                            continue  # out-of-bounds
                        for j_shift in SHIFTS:
                            if i_shift == 0 and j_shift == 0:
                                continue  # no shift
                            new_j = j + j_shift
                            if new_j < 0 or new_j >= new_flashes.shape[1]:
                                continue  # out-of-bounds
                            grid[new_i, new_j] += 1
    # each flashing one has its energy go back down
    for i in range(is_flashing.shape[0]):
        for j in range(is_flashing.shape[1]):
            if is_flashing[i, j]:
                grid[i, j] = RESET_LEVEL
    # how many flashed?
    n_flashed = is_flashing.sum()
    return n_flashed


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
    grid_backup = grid_.copy()
    # part 1
    flash_count = 0
    for _ in range(N_STEPS):
        flash_count += timestep(grid_)
    print(f"TOTAL flashes: {flash_count}")
    # part 2
    grid_ = grid_backup
    n_octopodes = grid_.size
    for step in count(start=1):
        count = timestep(grid_)
        if count == n_octopodes:
            print(f"ALL flash on step {step}")
            break
