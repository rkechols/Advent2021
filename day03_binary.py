import os
from typing import Callable, Dict, List

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input03.txt")

ZERO = "0"
ONE = "1"
DIGITS = [ZERO, ONE]


def select_digit(counts: Dict[str, List[int]], index: int, comparator: Callable[[int, int], bool]) -> str:
    best_count = None
    best_digit = None
    for digit in DIGITS:
        this_count = counts[digit][index]
        if best_count is None or comparator(this_count, best_count):
            best_count = this_count
            best_digit = digit
    return best_digit


if __name__ == "__main__":
    data = list()
    width = None
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            line = line_.strip()
            data.append(line)
            if width is None:
                width = len(line)
            else:
                assert width == len(line), "inconsistent row size in data"
    # part 1
    digit_counts = {digit: [0] * width for digit in DIGITS}
    for row in data:
        for i, digit in enumerate(row):
            digit_counts[digit][i] += 1
    gamma_rate_bin = list()
    epsilon_rate_bin = list()
    for i in range(width):
        best_digit_gamma = select_digit(digit_counts, i, lambda x, y: x > y)
        gamma_rate_bin.append(best_digit_gamma)
        best_digit_epsilon = select_digit(digit_counts, i, lambda x, y: x < y)
        epsilon_rate_bin.append(best_digit_epsilon)
    gamma_rate = int("".join(gamma_rate_bin), 2)
    epsilon_rate = int("".join(epsilon_rate_bin), 2)
    product = gamma_rate * epsilon_rate
    print(f"PRODUCT of gamma and epsilon: {product}")
