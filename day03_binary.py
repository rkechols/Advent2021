import os

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input03.txt")

ZERO = "0"
ONE = "1"
DIGITS = [ZERO, ONE]


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
    digit_counts = {digit: [0] * width for digit in DIGITS }
    for row in data:
        for i, digit in enumerate(row):
            digit_counts[digit][i] += 1
    gamma_rate_bin = list()
    epsilon_rate_bin = list()
    for i in range(width):
        best_count_gamma = None
        best_digit_gamma = None
        best_count_epsilon = None
        best_digit_epsilon = None
        for digit in DIGITS:
            this_count = digit_counts[digit][i]
            if best_count_gamma is None or this_count > best_count_gamma:
                best_count_gamma = this_count
                best_digit_gamma = digit
            if best_count_epsilon is None or this_count < best_count_epsilon:
                best_count_epsilon = this_count
                best_digit_epsilon = digit
        gamma_rate_bin.append(best_digit_gamma)
        epsilon_rate_bin.append(best_digit_epsilon)
    gamma_rate = int("".join(gamma_rate_bin), 2)
    epsilon_rate = int("".join(epsilon_rate_bin), 2)
    product = gamma_rate * epsilon_rate
    print(f"PRODUCT of gamma and epsilon: {product}")
