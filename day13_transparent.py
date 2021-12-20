import os
import re
from typing import Literal, Set, Tuple

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input13.txt")

INSTRUCTION_RE = re.compile(r"fold along ([xy])=(\d+)")
X = "x"
Y = "y"


def apply_fold(points: Set[Tuple[int, int]], axis: Literal["x", "y"], line_value: int) -> Set[Tuple[int, int]]:
    new_points = set()
    for x, y in points:
        if axis == X:
            if x < line_value:
                new_points.add((x, y))
            else:
                distance_from_line = x - line_value
                new_points.add((line_value - distance_from_line, y))
        elif axis == Y:
            if y < line_value:
                new_points.add((x, y))
            else:
                distance_from_line = y - line_value
                new_points.add((x, line_value - distance_from_line))
        else:
            raise ValueError(f"axis line_value must be 'x' or 'y', but received '{axis}'")
    return new_points


if __name__ == "__main__":
    points_ = set()
    instructions = list()
    reading_points = True
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            line = line_.strip()
            if line == "":
                reading_points = False
            elif reading_points:
                points_.add(tuple(map(int, line.split(","))))
            else:  # reading instructions
                match = INSTRUCTION_RE.fullmatch(line)
                if match is None:
                    raise ValueError(f"Could not match line:\n{line}")
                axis_, value_s = match.groups()
                value_ = int(value_s)
                instructions.append((axis_, value_))
    # part 1
    points_ = apply_fold(points_, *instructions[0])
    print(f"# POINTS after first fold: {len(points_)}")
    # part 2
    for i in range(1, len(instructions)):
        points_ = apply_fold(points_, *instructions[i])
    # print it like a canvas
    max_x = max(x_ for x_, _ in points_)
    max_y = max(y_ for _, y_ in points_)
    canvas = [["."] * (max_x + 1) for _ in range(max_y + 1)]
    for x_, y_ in points_:
        canvas[y_][x_] = "#"
    for row in canvas:
        print("".join(row))
