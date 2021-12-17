import os

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input02.txt")

FORWARD = "forward"
DOWN = "down"
UP = "up"


if __name__ == "__main__":
    directions = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line in f:
            direction, num = line.strip().split()
            num = int(num)
            directions.append((direction, num))
    # part 1
    depth = 0
    y_position = 0
    for direction, num in directions:
        if direction == FORWARD:
            y_position += num
        elif direction == DOWN:
            depth += num
        elif direction == UP:
            depth -= num
        else:
            raise ValueError(f"Unexpected direction: {direction}")
    print(f"FINAL DEPTH: {depth}")
    print(f"FINAL Y_POSITION: {y_position}")
    print(f"PRODUCT: {depth * y_position}")
    print("-----")
    # part 2
    depth = 0
    y_position = 0
    aim = 0
    for direction, num in directions:
        if direction == FORWARD:
            y_position += num
            depth += (aim * num)
        elif direction == DOWN:
            aim += num
        elif direction == UP:
            aim -= num
        else:
            raise ValueError(f"Unexpected direction: {direction}")
    print(f"FINAL DEPTH: {depth}")
    print(f"FINAL Y_POSITION: {y_position}")
    print(f"PRODUCT: {depth * y_position}")
