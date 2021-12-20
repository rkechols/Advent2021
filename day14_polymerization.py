import os
import re
from collections import Counter

from constants import INPUTS_DIR, UTF_8
from tqdm import tqdm


INPUT_FILE = os.path.join(INPUTS_DIR, "input14.txt")

RULE_RE = re.compile(r"([A-Z]{2}) -> ([A-Z])")
N_STEPS = 40  # 10 for part 1; 40 for part 2


if __name__ == "__main__":
    rules = dict()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        polymer = list(f.readline().strip())
        f.readline()  # skip the blank
        while (line_ := f.readline()) != "":
            line = line_.strip()
            match = RULE_RE.fullmatch(line)
            if match is None:
                raise ValueError(f"Could not match line:\n{line}")
            pair, result = match.groups()
            rules[pair] = result
    # synthesize
    for _ in tqdm(range(N_STEPS)):
        edited = list()
        for i in range(len(polymer) - 1):
            edited.append(polymer[i])
            pair = polymer[i] + polymer[i + 1]
            try:
                to_insert = rules[pair]
                edited.append(to_insert)
            except KeyError:
                pass  # no matching rule; no insertion
        edited.append(polymer[-1])
        polymer = edited
    # analyze
    char_counts = Counter(polymer)
    freq_biggest = None
    freq_smallest = None
    for count in char_counts.values():
        if freq_biggest is None or count > freq_biggest:
            freq_biggest = count
        if freq_smallest is None or count < freq_smallest:
            freq_smallest = count
    diff = freq_biggest - freq_smallest
    print(f"DIFF in frequencies: {diff}")
