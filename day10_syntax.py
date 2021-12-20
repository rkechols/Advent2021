import os
from collections import deque
from typing import Optional, Tuple

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input10.txt")

SYMBOL_MATCH_DATA = {
    ")": ("(", 3),
    "]": ("[", 57),
    "}": ("{", 1197),
    ">": ("<", 25137)
}
OPENERS = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}


if __name__ == "__main__":
    total_corrupt = 0
    incomplete_scores = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            line = line_.strip()
            # figure if it's corrupt or incomplete
            stack = deque()
            for c in line:
                if c in OPENERS:
                    stack.append(c)
                else:
                    needed_match, points = SYMBOL_MATCH_DATA[c]  # KeyError if it's an entirely unknown symbol
                    if len(stack) == 0 or stack.pop() != needed_match:
                        # corrupt
                        total_corrupt += points
                        break
            else:  # incomplete
                score_incomplete = 0
                while len(stack) > 0:
                    next_char = stack.pop()
                    points = OPENERS[next_char]
                    # update total score
                    score_incomplete *= 5
                    score_incomplete += points
                incomplete_scores.append(score_incomplete)
    print(f"TOTAL corrupt score: {total_corrupt}")
    incomplete_scores.sort()
    median = incomplete_scores[len(incomplete_scores) // 2]
    print(f"MEDIAN incomplete score: {median}")
