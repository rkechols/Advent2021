import os
import re
from typing import Dict, Tuple

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input05.txt")

LINE_RE = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")


if __name__ == "__main__":
    lines = list()
    min_x = min_y = max_x = max_y = None
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line in f:
            if (match := LINE_RE.fullmatch(line.strip())) is not None:
                x1, y1, x2, y2 = tuple(map(int, match.groups()))
                lines.append(((x1, y1), (x2, y2)))
                # maintain min values
                if min_x is None or x1 < min_x:
                    min_x = x1
                min_x = min(min_x, x2)
                if min_y is None or y1 < min_y:
                    min_y = y1
                min_y = min(min_y, y2)
                # maintain max values
                if max_x is None or x1 > max_x:
                    max_x = x1
                max_x = max(max_x, x2)
                if max_y is None or y1 > max_y:
                    max_y = y1
                max_y = max(max_y, y2)
            else:
                raise ValueError(f"could not parse line:\n{line}")
    # count spots for each tuple
    counter: Dict[Tuple[int, int], int] = dict()
    for (x1, y1), (x2, y2) in lines:
        if x1 == x2:
            if y1 < y2:
                y_range = range(y1, y2 + 1)
            else:
                y_range = range(y2, y1 + 1)
            for y in y_range:
                try:
                    counter[(x1, y)] += 1
                except KeyError:
                    counter[(x1, y)] = 1
        elif y1 == y2:
            if x1 < x2:
                x_range = range(x1, x2 + 1)
            else:
                x_range = range(x2, x1 + 1)
            for x in x_range:
                try:
                    counter[(x, y1)] += 1
                except KeyError:
                    counter[(x, y1)] = 1
        # TODO: else
    overlap_count = 0
    for count in counter.values():
        if count >= 2:
            overlap_count += 1
    print(f"OVERLAP count: {overlap_count}")


