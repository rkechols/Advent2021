import os
import re
from itertools import repeat
from typing import Dict, Tuple

from constants import INPUTS_DIR, UTF_8


USE_DIAGONALS = True  # False for part 1, True for part 2
INPUT_FILE = os.path.join(INPUTS_DIR, "input05.txt")

LINE_RE = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")


if __name__ == "__main__":
    lines = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line in f:
            if (match := LINE_RE.fullmatch(line.strip())) is not None:
                x1, y1, x2, y2 = tuple(map(int, match.groups()))
                lines.append(((x1, y1), (x2, y2)))
            else:
                raise ValueError(f"could not parse line:\n{line}")
    # count spots for each tuple
    counter: Dict[Tuple[int, int], int] = dict()
    for (x1, y1), (x2, y2) in lines:
        if x1 == x2 and y1 == y2:
            # special case of a single point so we don't get in an infinite loop
            try:
                counter[(x1, y1)] += 1
            except KeyError:
                counter[(x1, y1)] = 1
        # skip a diagonal if we need to
        if not USE_DIAGONALS and x1 != x2 and y1 != y2:
            continue
        # create an x iterable
        if x1 < x2:
            x_range = range(x1, x2 + 1)
        elif x2 < x1:
            x_range = range(x2, x1 + 1)
        else:
            x_range = repeat(x1)
        # create a y iterable
        if y1 < y2:
            y_range = range(y1, y2 + 1)
        elif y2 < y1:
            y_range = range(y2, y1 + 1)
        else:
            y_range = repeat(y1)
        # count the points
        for x, y in zip(x_range, y_range):
            try:
                counter[(x, y)] += 1
            except KeyError:
                counter[(x, y)] = 1
    overlap_count = 0
    for count in counter.values():
        if count >= 2:
            overlap_count += 1
    print(f"OVERLAP count: {overlap_count}")
