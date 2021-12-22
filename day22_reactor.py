import os
from typing import Tuple

import numpy as np
import re

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input22.txt")

RANGE_RE = re.compile(r"(-?\d+)\.\.(-?\d+)")
ON = "on"

SIZE = 101
SHIFT = 50


def parse_line(line: str) -> Tuple[bool, int, int, int, int, int, int]:
    on_off, loc = line.split()
    power = (on_off == ON)
    x_loc_str, y_loc_str, z_loc_str = loc.split(",")
    x_low, x_high = map(int, RANGE_RE.search(x_loc_str).groups())
    y_low, y_high = map(int, RANGE_RE.search(y_loc_str).groups())
    z_low, z_high = map(int, RANGE_RE.search(z_loc_str).groups())
    return power, x_low, x_high, y_low, y_high, z_low, z_high


def part1():
    grid = np.zeros((SIZE, SIZE, SIZE), dtype=bool)
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            power, x_low, x_high, y_low, y_high, z_low, z_high = parse_line(line_.strip())
            x_low += SHIFT
            x_high += SHIFT + 1
            if x_low < 0 or x_high >= SIZE:
                continue  # skip
            y_low += SHIFT
            y_high += SHIFT + 1
            if y_low < 0 or y_high >= SIZE:
                continue  # skip
            z_low += SHIFT
            z_high += SHIFT + 1
            if z_low < 0 or z_high >= SIZE:
                continue  # skip
            # perform the switch
            grid[x_low:x_high, y_low:y_high, z_low:z_high] = power
    n_spots_on = grid.sum()
    print(f"NUMBER cubes ON: {n_spots_on}")


if __name__ == "__main__":
    part1()
