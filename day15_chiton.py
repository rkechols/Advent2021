import heapq
import os
import sys
from copy import copy
from typing import Iterable, Set, Tuple

import numpy as np

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input15.txt")

LOWEST_SINGLE_COST = 1
HIGHEST_SINGLE_COST = 9


def get_lower_bound(min_moves_left: int, cost: int) -> int:
    cost_left = min_moves_left * LOWEST_SINGLE_COST
    lower_bound = cost + cost_left
    return lower_bound


class Path:
    def __init__(self, i: int, j: int, cost: int, lower_bound: int, visited: Set[Tuple[int, int]], min_moves_left: int):
        self.i = i
        self.j = j
        self.cost = cost
        self.lower_bound = lower_bound
        self.visited = visited
        self.min_moves_left = min_moves_left
        self.sort_heuristic = lower_bound + (min_moves_left * HIGHEST_SINGLE_COST)

    def __lt__(self, other) -> bool:
        assert isinstance(other, self.__class__), f"cannot compare {self.__class__.__name__} with other class {other.__class__.__name__}"
        return self.sort_heuristic < other.sort_heuristic


class Solver:
    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.rows = grid.shape[0]
        self.cols = grid.shape[1]

    def greedy(self) -> int:
        i = j = 0
        total = 0
        while i < self.rows - 1 and j < self.cols - 1:
            right = self.grid[i, j + 1]
            down = self.grid[i + 1, j]
            if right < down:
                j += 1
            else:
                i += 1
            total += self.grid[i, j]
        # we've hit one edge, now slide along the edge to the finish
        while i < self.rows - 1:
            i += 1
            total += self.grid[i, j]
        while j < self.cols - 1:
            j += 1
            total += self.grid[i, j]
        # how much does this one cost
        return total

    def get_min_moves_left(self, i: int, j: int) -> int:
        return (self.rows - (i + 1)) + (self.cols - (j + 1))

    def get_children(self, path: Path) -> Iterable[Path]:
        for i_shift, j_shift in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_loc = (path.i + i_shift, path.j + j_shift)
            if 0 <= next_loc[0] < self.rows and 0 <= next_loc[1] < self.cols:
                new_cost = path.cost + self.grid[next_loc]
                mml = self.get_min_moves_left(*next_loc)
                lower_bound = get_lower_bound(mml, new_cost)
                new_visited = copy(path.visited)
                new_visited.add(next_loc)
                new_path = Path(next_loc[0], next_loc[1], new_cost, lower_bound, new_visited, mml)
                yield new_path

    # branch and bound
    def solve(self) -> int:
        pruned = 0
        n_longest = 0
        # get a quick baseline
        best_cost = self.greedy()
        # set up a priority queue with starting state
        heap = list()
        min_left = self.get_min_moves_left(0, 0)
        heapq.heappush(heap, Path(0, 0, 0, get_lower_bound(min_left, 0), {(0, 0)}, min_left))
        while len(heap) > 0:
            n_longest = max(n_longest, len(heap))
            partial_path = heapq.heappop(heap)
            if partial_path.lower_bound > best_cost:
                pruned += 1
                continue  # lost cause; don't make its children
            for next_partial_path in self.get_children(partial_path):
                if next_partial_path.i + 1 == self.rows and next_partial_path.j + 1 == self.cols:
                    # this is a full path (potential solution)
                    if next_partial_path.cost < best_cost:  # did it beat the best we've seen?
                        best_cost = next_partial_path.cost
                else:
                    # if it has potential to beat the best solution, put it in the queue
                    if next_partial_path.lower_bound < best_cost:
                        heapq.heappush(heap, next_partial_path)
                    else:
                        pruned += 1
        # the best we've got
        print(f"PRUNED: {pruned}", file=sys.stderr)
        print(f"LONGEST Q: {n_longest}", file=sys.stderr)
        return best_cost


if __name__ == "__main__":
    lines = list()
    line_len = None
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            line = line_.strip()
            if line_len is None:
                line_len = len(line)
            else:
                assert len(line) == line_len, "line lengths not consistent?"
            lines.append(list(line))
    n_lines = len(lines)
    grid_ = np.empty((n_lines, line_len), dtype=int)
    for i_, line in enumerate(lines):
        for j_, num_char in enumerate(line):
            grid_[i_, j_] = int(num_char)
    # run a greedy search to get some baseline
    solver = Solver(grid_)
    best_cost_ = solver.solve()
    print(f"BEST cost: {best_cost_}")
