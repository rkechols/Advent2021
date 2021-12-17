import os

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input07.txt")


if __name__ == "__main__":
    crabs = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line in f:
            crabs.extend(map(int, line.strip().split(",")))
    crabs.sort()
    n_crabs = len(crabs)
    low = crabs[0]
    high = crabs[-1]
    best_position = low
    best_cost = sum(abs(x - low) for x in crabs)
    cost = best_cost
    index = 0
    for position in range(low + 1, high + 1):
        # move one position to the right; find which crab I'm lined up with
        while index < n_crabs and crabs[index] < position:
            index += 1
        # add 1 for each crab that's to the left, and
        # subtract 1 for each crab that's here or to the right
        cost += (index - (n_crabs - index))
        if cost < best_cost:
            best_cost = cost
            best_position = position
    print(f"BEST COST: {best_cost}")
    print(f"(from position {best_position})")
