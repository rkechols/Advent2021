import os

import numpy as np

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input20.txt")
N_ITERATIONS = 50  # set to 2 for part 1; set to 50 for part 2

LIGHT = "#"
DARK = "."


def get_kernel_val(image: np.ndarray, i: int, j: int, oob_value: bool) -> int:
    digits = list()
    for i_shift in [-1, 0, 1]:
        new_i = i + i_shift
        for j_shift in [-1, 0, 1]:
            new_j = j + j_shift
            if new_i < 0 or new_i >= image.shape[0] or new_j < 0 or new_j >= image.shape[1]:
                bool_value = oob_value
            else:
                bool_value = image[new_i, new_j]
            digit = "1" if bool_value else "0"
            digits.append(digit)
    value = int("".join(digits), base=2)
    return value


if __name__ == "__main__":
    image_ = list()
    n_cols = None
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        algorithm = f.readline().strip()
        f.readline()  # skip blank line
        while (line_ := f.readline()) != "":
            row_ = list(line_.strip())
            row_len = len(row_)
            if n_cols is None:
                n_cols = row_len
            else:
                assert n_cols == row_len, "inconsistent row length?"
            image_.append(row_)
    algorithm = [c == LIGHT for c in algorithm]
    n_rows = len(image_)
    image_np = np.empty((n_rows, n_cols), dtype=bool)
    for i_ in range(n_rows):
        for j_ in range(n_cols):
            image_np[i_, j_] = (image_[i_][j_] == LIGHT)
    image_ = image_np
    background = False
    # enhance the image
    for _ in range(N_ITERATIONS):
        # add padding
        n_rows += 2
        n_cols += 2
        expanded_image = np.empty((n_rows, n_cols), dtype=bool)
        expanded_image[0, :] = background
        expanded_image[-1, :] = background
        expanded_image[:, 0] = background
        expanded_image[:, -1] = background
        expanded_image[1:-1, 1:-1] = image_
        image_ = expanded_image
        # calculate the next step
        new_image = np.empty_like(image_)
        for i_ in range(n_rows):
            for j_ in range(n_cols):
                alg_index = get_kernel_val(image_, i_, j_, background)
                new_val = algorithm[alg_index]
                new_image[i_, j_] = new_val
        image_ = new_image
        # also figure out what happens to the infinite background
        if background:  # 9 light pixels -> biggest/last index
            background = algorithm[-1]
        else:  # 9 dark pixels -> smallest/first index
            background = algorithm[0]
    n_light = image_.sum()
    print(f"NUMBER of light pixels: {n_light}")
