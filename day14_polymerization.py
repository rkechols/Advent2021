import os
import re

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input14.txt")

RULE_RE = re.compile(r"([A-Z]{2}) -> ([A-Z])")
N_STEPS = 40  # 10 for part 1; 40 for part 2


if __name__ == "__main__":
    rules = dict()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        polymer = f.readline().strip()
        f.readline()  # skip the blank
        while (line_ := f.readline()) != "":
            line = line_.strip()
            match = RULE_RE.fullmatch(line)
            if match is None:
                raise ValueError(f"Could not match line:\n{line}")
            pair, result = match.groups()
            rules[pair] = result
    # initialize
    pair_counts = dict()
    for i in range(len(polymer) - 1):
        pair = polymer[i:i+2]
        try:
            pair_counts[pair] += 1
        except KeyError:
            pair_counts[pair] = 1
    # synthesize (keeping counts of each char-pair type)
    for _ in range(N_STEPS):
        pair_counts_new = dict()
        for pair, count in pair_counts.items():
            try:
                to_insert = rules[pair]
            except KeyError:
                # no replacement; all instances stay unchanged
                pair_counts_new[pair] = count
            else:
                # left char with inserted
                new_pair1 = pair[0] + to_insert
                try:
                    pair_counts_new[new_pair1] += count
                except KeyError:
                    pair_counts_new[new_pair1] = count
                # inserted with right char
                new_pair2 = to_insert + pair[1]
                try:
                    pair_counts_new[new_pair2] += count
                except KeyError:
                    pair_counts_new[new_pair2] = count
        # update 'current'
        pair_counts = pair_counts_new
    # count how many of each individual char
    char_counts = dict()
    for pair, count in pair_counts.items():
        first_char = pair[0]  # only the first is needed since including the second would double-count it
        try:
            char_counts[first_char] += count
        except KeyError:
            char_counts[first_char] = count
    # the last character gets missed if you just go by the pairs
    try:
        char_counts[polymer[-1]] += 1
    except KeyError:
        char_counts[polymer[-1]] = 1
    # what are the most and least frequent?
    freq_biggest = None
    freq_smallest = None
    for count in char_counts.values():
        if freq_biggest is None or count > freq_biggest:
            freq_biggest = count
        if freq_smallest is None or count < freq_smallest:
            freq_smallest = count
    diff = freq_biggest - freq_smallest
    print(f"DIFF in frequencies: {diff}")
