import os
from collections import Counter
from itertools import chain
from typing import List

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input08.txt")


SEGMENT_COUNT_TO_OPTIONS = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8],
}
COUNTS_OBVIOUS = {2, 3, 4, 7}
COUNTS_DIFFICULT = {5, 6}
SEGMENT_TOTAL_COUNT_TO_SEGMENT = {
    6: "b",
    8: "c",  # also "a", but we have a different way to figure out "a"
    4: "e",
    9: "f"
}
TRUE_SEGS_TO_DIGIT = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9"
}


def decode(in_values: List[str], out_values: List[str]) -> int:
    solved_segments = dict()
    easies = dict()
    for val in in_values:
        val_len = len(val)
        if val_len in COUNTS_OBVIOUS:
            digit = SEGMENT_COUNT_TO_OPTIONS[val_len][0]
            easies[digit] = set(val)
    solved_segments[next(iter(easies[7] - easies[1]))] = "a"
    seg_to_total_count = Counter(chain(*in_values))
    false_segs_for_d_g = set()
    for false_seg, count in seg_to_total_count.items():
        if count == 7:
            false_segs_for_d_g.add(false_seg)
        elif count in SEGMENT_TOTAL_COUNT_TO_SEGMENT:
            if solved_segments.get(false_seg, None) is not None:
                continue  # skip whatever maps to "a"
            true_seg = SEGMENT_TOTAL_COUNT_TO_SEGMENT[count]
            solved_segments[false_seg] = true_seg
    # if it's in false_segs_for_d_g and used in a 4, it's segment d
    false_for_d = next(iter(easies[4] & false_segs_for_d_g))
    solved_segments[false_for_d] = "d"
    # the other one has to be g
    solved_segments[next(iter(false_segs_for_d_g - {false_for_d}))] = "g"
    # all segments solved; convert the outputs
    true_outputs = ["".join(solved_segments[x] for x in val) for val in out_values]
    # get the actual digits
    digits = [TRUE_SEGS_TO_DIGIT["".join(sorted(val))] for val in true_outputs]
    # convert the digits to an int
    to_return = int("".join(digits))
    return to_return


if __name__ == "__main__":
    easy_count = 0
    total = 0
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line in f:
            in_text, out_text = line.split("|")
            in_values_ = in_text.strip().split()
            out_values_ = out_text.strip().split()
            for out_val in out_values_:
                if len(SEGMENT_COUNT_TO_OPTIONS[len(out_val)]) == 1:
                    easy_count += 1
            value = decode(in_values_, out_values_)
            total += value
    print(f"EASY COUNT: {easy_count}")
    print(f"TOTAL VALUE: {total}")
