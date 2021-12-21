import os
from typing import Optional, Tuple

from constants import INPUTS_DIR, UTF_8
import re


INPUT_FILE = os.path.join(INPUTS_DIR, "input17.txt")

X_RE = re.compile(r"x=(-?\d+)\.\.(-?\d+)")
Y_RE = re.compile(r"y=(-?\d+)\.\.(-?\d+)")


def trajectory_highest_y(x_velo: int, y_velo: int, target_x: Tuple[int, int], target_y: Tuple[int, int]) -> Optional[int]:
    x = y = 0  # start position
    highest = 0
    while True:  # "gravity" guarantees this will terminate
        if target_x[0] <= x <= target_x[1] and target_y[0] <= y <= target_y[1]:
            # we're in the box
            return highest
        # check if we missed the box
        if (x_velo < 0 and x < target_x[0]) or (x_velo > 0 and x > target_x[1]):
            return None
        if y_velo < 0 and y < target_y[0]:
            return None
        # increment by 1 time step
        x += x_velo
        y += y_velo
        highest = max(highest, y)
        if x_velo < 0:
            x_velo += 1
        elif x_velo > 0:
            x_velo -= 1
        y_velo -= 1


if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        content = f.read()
    x_low, x_high = map(int, X_RE.search(content).groups())
    if x_low > x_high:
        x_low, x_high = x_high, x_low
    target_x_ = (x_low, x_high)
    y_low, y_high = map(int, Y_RE.search(content).groups())
    if y_low > y_high:
        y_low, y_high = y_high, y_low
    target_y_ = (y_low, y_high)
    # TODO
