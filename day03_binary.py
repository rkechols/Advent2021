import os
from typing import Callable, Dict, Iterable, List

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input03.txt")

ZERO = "0"
ONE = "1"
DIGITS = [ZERO, ONE]


def most_common_comparator(x: int, y: int) -> bool:
    return x > y


def least_common_comparator(x: int, y: int) -> bool:
    return x < y


def count_digits(binaries: Iterable[str]) -> Dict[str, List[int]]:
    counts = {digit: [0] * width for digit in DIGITS}
    for binary in binaries:
        for i, digit in enumerate(binary):
            counts[digit][i] += 1
    return counts


def break_ties(counts: Dict[str, List[int]]):
    # TODO: this function is not generalized for more than 2 digits
    for i in range(width):
        if counts[ZERO][i] == counts[ONE][i]:
            counts[ONE][i] += 1


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
        for i_, digit in enumerate(row):
            digit_counts[digit][i_] += 1
    gamma_rate_bin = list()
    epsilon_rate_bin = list()
    for i_ in range(width):
        most_common_digit = select_digit(digit_counts, i_, most_common_comparator)
        gamma_rate_bin.append(most_common_digit)
        least_common_digit = select_digit(digit_counts, i_, least_common_comparator)
        epsilon_rate_bin.append(least_common_digit)
    gamma_rate = int("".join(gamma_rate_bin), 2)
    epsilon_rate = int("".join(epsilon_rate_bin), 2)
    product = gamma_rate * epsilon_rate
    print(f"PRODUCT of gamma and epsilon: {product}")
    # part 2
    # get oxygen rating
    oxygen_options = set(data)
    for i_ in range(width):
        if len(oxygen_options) <= 1:
            break  # we're done!
        # re-count digits
        digit_counts = count_digits(oxygen_options)
        break_ties(digit_counts)
        # keep only ones with the most common digit in this place
        most_common_digit = select_digit(digit_counts, i_, most_common_comparator)
        new_options = set()
        for option in oxygen_options:
            if option[i_] == most_common_digit:
                new_options.add(option)
        oxygen_options = new_options
    oxygen = int(oxygen_options.pop(), 2)
    # get CO2 rating
    co2_options = set(data)
    for i_ in range(width):
        if len(co2_options) <= 1:
            break  # we're done!
        # re-count digits
        digit_counts = count_digits(co2_options)
        break_ties(digit_counts)
        # keep only ones with the least common digit in this place
        least_common_digit = select_digit(digit_counts, i_, least_common_comparator)
        new_options = set()
        for option in co2_options:
            if option[i_] == least_common_digit:
                new_options.add(option)
        co2_options = new_options
    co2 = int(co2_options.pop(), 2)
    # answer
    life_support = oxygen * co2
    print(f"PRODUCT of oxygen and CO2: {life_support}")
