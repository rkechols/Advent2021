import os
from collections import Counter, defaultdict

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input06.txt")
N_DAYS = 256  # 80 for part 1, and 256 for part 2
AGE_RESET = 6
AGE_SPAWN = 8


if __name__ == "__main__":
    fish = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line in f:
            fish.extend(map(int, line.strip().split(",")))
    counter = Counter(fish)
    counter = defaultdict(lambda: 0, counter)
    # simulate
    for _ in range(N_DAYS):
        new_counter = dict()
        # move all the fish down one (except 0)
        for age in range(AGE_SPAWN):
            new_counter[age] = counter[age + 1]
        # fish at 0 go up to AGE_RESET, and make new fish at AGE_SPAWN
        n_spawn = counter[0]
        new_counter[AGE_RESET] += n_spawn
        new_counter[AGE_SPAWN] = n_spawn
        # perform the update
        counter = new_counter
    total_fish = sum(counter.values())
    print(f"TOTAL FISH: {total_fish}")
