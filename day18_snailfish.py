import os
import re
from typing import List, Tuple, Union

from constants import INPUTS_DIR, UTF_8


SFNumber = Union[List, int]


INPUT_FILE = os.path.join(INPUTS_DIR, "input18.txt")

EXPLODE_DEPTH = 4
NUMBER_RE = re.compile(r"\d+")
MULTI_DIGIT_NUM_RE = re.compile(r"\d{2,}")
PLAIN_PAIR_RE = re.compile(r"\[(\d+),\s*(\d+)]")


def is_plain_pair(sf_num: SFNumber) -> bool:
    if not isinstance(sf_num, list):
        return False
    assert len(sf_num) == 2, "all SFNumbers should be length 2"
    left, right = sf_num
    if not isinstance(left, int):
        return False
    if not isinstance(right, int):
        return False
    return True


def explode(sf_num: SFNumber) -> SFNumber:
    sf_num_str = str(sf_num)
    stack_depth = 0
    for i in range(len(sf_num_str)):
        if stack_depth >= 4 and (match := PLAIN_PAIR_RE.match(sf_num_str, pos=i)) is not None:
            # we can explode!
            left_num, right_num = map(int, match.groups())
            # add the left part to the nearest number in the preceding section
            before = sf_num_str[:match.start()]
            preceding_number_span = None
            for num_match in NUMBER_RE.finditer(before):
                preceding_number_span = num_match.span()
            if preceding_number_span is not None:  # make sure we found any preceding number
                start, end = preceding_number_span
                # calculate the sum of the left and the preceding
                preceding_number = int(before[start:end])
                new_number = preceding_number + left_num
                # replace the preceding with the sum
                before = before[:start] + str(new_number) + before[end:]
            # replace the pair itself with a 0
            middle = "0"
            # add the right part to the nearest number in the following section
            after = sf_num_str[match.end():]
            if (num_match := NUMBER_RE.search(after)) is not None:  # make sure we found any following number
                start, end = num_match.span()
                # calculate the sum of the right and the following
                following_number = int(after[start:end])
                new_number = following_number + right_num
                # replace the preceding with the sum
                after = after[:start] + str(new_number) + after[end:]
            # stick them all together
            sf_num_str = before + middle + after
            break  # only do the one explode
        # keep looking for a place to explode
        c = sf_num_str[i]
        if c == "[":
            stack_depth += 1
        elif c == "]":
            stack_depth -= 1
    sf_num = eval(sf_num_str)
    return sf_num


def split_num(x: int) -> Tuple[int, int]:
    left = x // 2
    right = x - left
    return left, right


def split(sf_num: SFNumber) -> SFNumber:
    sf_num_str = str(sf_num)
    if (match := MULTI_DIGIT_NUM_RE.search(sf_num_str)) is not None:
        start, end = match.span()
        # get the stuff before
        before = sf_num_str[:start]
        # get the new middle
        value = int(match.group(0))
        middle = str(list(split_num(value)))
        # get the stuff after
        after = sf_num_str[end:]
        # put it all together
        sf_num_str = before + middle + after
        sf_num = eval(sf_num_str)
    return sf_num


def reduce(sf_num: SFNumber) -> SFNumber:
    while True:
        # try exploding
        new_sf_num = explode(sf_num)
        if sf_num != new_sf_num:  # explode worked
            sf_num = new_sf_num
            continue
        # no explode
        # try splitting
        new_sf_num = split(sf_num)
        if sf_num != new_sf_num:  # split worked
            sf_num = new_sf_num
            continue
        # no split
        break
    return sf_num


def magnitude(sf_num: SFNumber) -> int:
    if isinstance(sf_num, int):
        return sf_num
    left, right = sf_num
    return (3 * magnitude(left)) + (2 * magnitude(right))


if __name__ == "__main__":
    numbers = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            snailfish_num = eval(line_.strip())
            numbers.append(snailfish_num)
    # add them all up
    snailfish_sum = numbers[0]
    for i_ in range(1, len(numbers)):
        snailfish_sum = [snailfish_sum, numbers[i_]]
        snailfish_sum = reduce(snailfish_sum)
    print(f"SUM: {snailfish_sum}")
    # get the magnitude
    mag = magnitude(snailfish_sum)
    print(f"MAGNITUDE of sum: {mag}")
    print("------")
    # part 2
    best_mag = None
    for num1 in numbers:
        for num2 in numbers:
            snailfish_sum = [num1, num2]
            snailfish_sum = reduce(snailfish_sum)
            mag = magnitude(snailfish_sum)
            if best_mag is None or mag > best_mag:
                best_mag = mag
    print(f"BIGGEST magnitude: {best_mag}")
