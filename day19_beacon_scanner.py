import os
import re
from typing import Optional, Set, Tuple

import numpy as np
from tqdm import tqdm

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input19.txt")

SCANNER_RE = re.compile(r"--- scanner (\d+) ---")
OVERLAP_THRESHOLD = 12

ORIENTATION_MATRICES = [
    np.array([  # identity
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]),
    np.array([  # 90 degrees about x
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]
    ]),
    np.array([  # 180 degrees about x
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, -1]
    ]),
    np.array([  # 270 degrees about x
        [1, 0, 0],
        [0, 0, 1],
        [0, -1, 0]
    ]),

    # +y becomes +x axis
    np.array([
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0]
    ]),
    np.array([
        [0, 1, 0],
        [-1, 0, 0],
        [0, 0, 1]
    ]),
    np.array([
        [0, 1, 0],
        [0, 0, -1],
        [-1, 0, 0]
    ]),
    np.array([
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, -1]
    ]),

    # +z becomes +x axis
    np.array([
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0]
    ]),
    np.array([
        [0, 0, 1],
        [0, -1, 0],
        [1, 0, 0]
    ]),
    np.array([
        [0, 0, 1],
        [-1, 0, 0],
        [0, -1, 0]
    ]),
    np.array([
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0]
    ]),

    # -x becomes +x axis (180 about z)
    np.array([
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ]),
    np.array([
        [-1, 0, 0],
        [0, 0, 1],
        [0, 1, 0]
    ]),
    np.array([
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, -1]
    ]),
    np.array([
        [-1, 0, 0],
        [0, 0, -1],
        [0, -1, 0]
    ]),

    # -y becomes +x axis
    np.array([
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ]),
    np.array([
        [0, -1, 0],
        [0, 0, -1],
        [1, 0, 0]
    ]),
    np.array([
        [0, -1, 0],
        [-1, 0, 0],
        [0, 0, -1]
    ]),
    np.array([
        [0, -1, 0],
        [0, 0, 1],
        [-1, 0, 0]
    ]),

    # -z becomes +x axis
    np.array([
        [0, 0, -1],
        [0, 1, 0],
        [1, 0, 0]
    ]),
    np.array([
        [0, 0, -1],
        [-1, 0, 0],
        [0, 1, 0]
    ]),
    np.array([
        [0, 0, -1],
        [0, -1, 0],
        [-1, 0, 0]
    ]),
    np.array([
        [0, 0, -1],
        [1, 0, 0],
        [0, -1, 0]
    ]),
]


def apply_orientation_single(orientation: np.ndarray, xyz: Tuple[int, int, int]) -> Tuple[int, int, int]:
    xyz_vector = np.array(xyz)
    new_xyz_vector = orientation.dot(xyz_vector)
    new_xyz = tuple(new_xyz_vector)
    return new_xyz


def apply_orientation(orientation: np.ndarray, points: Set[Tuple[int, int, int]]) -> Set[Tuple[int, int, int]]:
    new_set = set()
    for point in points:
        new_set.add(apply_orientation_single(orientation, point))
    return new_set


def align_points(points_fixed: Set[Tuple[int, int, int]],
                 points_to_adjust: Set[Tuple[int, int, int]]
                 ) -> Optional[Tuple[Set[Tuple[int, int, int]], Tuple[int, int, int]]]:
    points_fixed_list = list(points_fixed)
    points_fixed_list.sort()
    points_to_adjust_list = list(points_to_adjust)
    points_to_adjust_list.sort()
    attempted = set()
    for i in range(len(points_fixed_list) + 1 - OVERLAP_THRESHOLD):
        first_fixed_point = points_fixed_list[i]
        for j in range(len(points_to_adjust_list) + 1 - OVERLAP_THRESHOLD):
            first_point_to_adjust = points_to_adjust_list[j]
            # try aligning with this pair
            delta = tuple(first_fixed_point[k] - first_point_to_adjust[k] for k in range(3))
            if delta in attempted:
                continue  # already tried it
            attempted.add(delta)
            points_adjusted = set()
            for point in points_to_adjust_list:
                new_point = tuple(point[k] + delta[k] for k in range(3))
                points_adjusted.add(new_point)
            # is the overlap sufficient?
            overlap = points_fixed & points_adjusted
            if len(overlap) >= OVERLAP_THRESHOLD:
                return points_adjusted, delta
    return None


def manhattan_distance(p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> int:
    total = 0
    for i in range(3):
        total += abs(p1[i] - p2[i])
    return total


if __name__ == "__main__":
    all_data = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            line = line_.strip()
            if line == "":
                continue
            if SCANNER_RE.fullmatch(line) is not None:
                all_data.append(set())
            else:
                t = tuple(map(int, line.split(",")))
                all_data[-1].add(t)
    n_data = len(all_data)
    # align all the chunks
    fixed_beacons = [all_data[0]]
    aligned = {0}
    sensor_positions = [(0, 0, 0)]
    with tqdm(total=n_data) as progress:
        progress.update()
        while len(aligned) < n_data:
            # try to find a pair (1 from fixed, 1 from remaining) that we can align with sufficient overlap
            found = False
            for i_ in range(n_data):  # first pick a remaining one
                if i_ in aligned:
                    continue  # already got this one; not actually "remaining"
                new_beacons_original = all_data[i_]  # this is new the one we attempt to align
                for fixed_beacon_set in fixed_beacons:  # try it with each fixed one
                    for orientation_ in ORIENTATION_MATRICES:  # try all 16 orientations
                        new_beacons = apply_orientation(orientation_, new_beacons_original)
                        alignment = align_points(fixed_beacon_set, new_beacons)
                        if alignment is not None:  # sufficient overlap to align
                            new_beacons, sensor_pos = alignment
                            fixed_beacons.append(new_beacons)
                            aligned.add(i_)
                            sensor_positions.append(sensor_pos)
                            found = True  # cascade the break
                            progress.update()
                            break
                    if found:
                        break
                if found:
                    break
            if not found:
                raise ValueError("could not find any alignment")
    # collapse the sections to a unified representation
    all_beacons_aligned = set()
    for beacon_set in fixed_beacons:
        all_beacons_aligned.update(beacon_set)
    n_all_beacons_aligned = len(all_beacons_aligned)
    print(f"NUMBER of beacons: {n_all_beacons_aligned}")
    # part 2
    n_sensors = len(sensor_positions)
    biggest = None
    for i_ in range(n_sensors - 1):
        p1_ = sensor_positions[i_]
        for j_ in range(i_ + 1, n_sensors):
            p2_ = sensor_positions[j_]
            m_distance = manhattan_distance(p1_, p2_)
            if biggest is None or m_distance > biggest:
                biggest = m_distance
    print(f"GREATEST distance between two: {biggest}")
