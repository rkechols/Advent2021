import os
import sys
from typing import Dict, List, Set

from constants import INPUTS_DIR, UTF_8


Graph = Dict[str, Set[str]]


INPUT_FILE = os.path.join(INPUTS_DIR, "input12.txt")

START = "start"
END = "end"


def dfs_part1(graph: Graph, current: str, path: List[str]) -> int:
    if current == END:
        return 1
    path.append(current)
    mini_total = 0
    for neighbor in graph[current]:
        if neighbor.islower() and neighbor in path:
            # it's little, and we already visited; can't go through it again
            continue
        mini_total += dfs_part1(graph, neighbor, path)
    path.pop()  # remove the current location from the end of the path before backing up
    return mini_total


def dfs_part2(graph: Graph, current: str, path: List[str], has_used_double_small: bool) -> int:
    if current == END:
        return 1
    path.append(current)
    mini_total = 0
    for neighbor in graph[current]:
        if neighbor == START:
            continue  # never try to go back to start
        if neighbor.islower() and neighbor in path:
            if has_used_double_small:
                continue  # to visit this one again we'd need our one double-use, but we already used it
            else:
                now_has_used_double_small = True
        else:  # it's upper or it's not in the path
            now_has_used_double_small = has_used_double_small
        mini_total += dfs_part2(graph, neighbor, path, now_has_used_double_small)
    path.pop()  # remove the current location from the end of the path before backing up
    return mini_total


if __name__ == "__main__":
    graph_ = dict()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line in f:
            c1, c2 = line.strip().split("-")
            if c1.isupper() and c2.isupper():
                print(f"WARNING - caves {c1} and {c2} are connected and both large; this will result in infinite paths to count!", file=sys.stderr)
            if c1 not in graph_:
                graph_[c1] = set()
            graph_[c1].add(c2)
            if c2 not in graph_:
                graph_[c2] = set()
            graph_[c2].add(c1)
    # part 1
    n_paths = dfs_part1(graph_, START, list())
    print(f"TOTAL paths possible: {n_paths}")
    print("-----")
    # part 2
    n_paths = dfs_part2(graph_, START, list(), False)
    print(f"TOTAL paths possible (with a double small allowed): {n_paths}")
