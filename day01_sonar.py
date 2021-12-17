import os

from constants import INPUTS_DIR, UTF_8
from collections import deque


INPUT_FILE = os.path.join(INPUTS_DIR, "input01-1.txt")


if __name__ == "__main__":
    numbers = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line in f:
            num = int(line.strip())
            numbers.append(num)
    n = len(numbers)
    # part 1
    count = 0
    for i in range(1, n):
        if numbers[i] > numbers[i - 1]:
            count += 1
    print(f"PART 1: number of increases: {count}")
    # part 2
    count = 0
    window = deque()
    window_sum = 0
    assert n > 3, "not enough data do do a sliding window of size 3"
    for i in range(3):
        x = numbers[i]
        window.append(x)
        window_sum += x
    for i in range(3, n):
        x = numbers[i]
        window.append(x)
        to_toss = window.popleft()
        prev_sum = window_sum
        window_sum += (x - to_toss)
        if window_sum > prev_sum:
            count += 1
    print(f"PART 2: number of increases: {count}")
