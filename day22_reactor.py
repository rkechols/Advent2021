import os
import re
from typing import Optional, Tuple

import numpy as np

from constants import INPUTS_DIR, UTF_8


SMALL_VERSION = False  # True for part 1, and False for part 2
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


def range_intersection(range1: Tuple[int, int], range2: Tuple[int, int]) -> Tuple[int, int]:
    return max(range1[0], range2[0]), min(range1[1], range2[1])


class Region:
    def __init__(self, x_low: int, x_high: int, y_low: int, y_high: int, z_low: int, z_high: int):
        self.x_low = x_low
        self.x_high = x_high
        self.y_low = y_low
        self.y_high = y_high
        self.z_low = z_low
        self.z_high = z_high
        self._neg_regions = list()

    def intersection(self, other) -> Optional[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
        assert isinstance(other, self.__class__), f"cannot 'and' with {other.__class__.__name__}"
        x_range = range_intersection((self.x_low, self.x_high), (other.x_low, other.x_high))
        if x_range[1] < x_range[0]:
            return None
        y_range = range_intersection((self.y_low, self.y_high), (other.y_low, other.y_high))
        if y_range[1] < y_range[0]:
            return None
        z_range = range_intersection((self.z_low, self.z_high), (other.z_low, other.z_high))
        if z_range[1] < z_range[0]:
            return None
        return x_range, y_range, z_range

    def add_neg_region(self, r: 'Region'):
        # does the new region overlap with any old ones?
        for existing_region in self._neg_regions:
            if (intersection := r.intersection(existing_region)) is not None:
                x_range, y_range, z_range = intersection
                r_overlap = Region(*x_range, *y_range, *z_range)
                # make sure the overlap isn't counted negative twice (only once)
                existing_region.add_neg_region(r_overlap)
        self._neg_regions.append(r)

    def count(self) -> int:
        # numbers given are inclusive on both ends, (for example, 2..4 is size 1+4-2 = 3)
        cell_count = (1 + self.x_high - self.x_low) * (1 + self.y_high - self.y_low) * (1 + self.z_high - self.z_low)
        for neg_region in self._neg_regions:
            cell_count -= neg_region.count()
        return cell_count


def part2():
    regions = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            power, x_low, x_high, y_low, y_high, z_low, z_high = parse_line(line_.strip())
            r = Region(x_low, x_high, y_low, y_high, z_low, z_high)
            # does the new region overlap with any old ones?
            for existing_region in regions:
                if (intersection := r.intersection(existing_region)) is not None:
                    x_range, y_range, z_range = intersection
                    r_overlap = Region(*x_range, *y_range, *z_range)
                    # if the new region is an "off", the overlap should not be counted at all
                    # if the new region is an "on", the overlap should not be double-counted
                    existing_region.add_neg_region(r_overlap)
            if power:
                regions.append(r)
    total = 0
    for r in regions:
        total += r.count()
    print(f"NUMBER cubes ON: {total}")


if __name__ == "__main__":
    if SMALL_VERSION:
        part1()
    else:
        part2()
