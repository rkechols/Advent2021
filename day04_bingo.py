import os
from typing import List, Optional

from constants import INPUTS_DIR, UTF_8


Board = List[List[Optional[int]]]


INPUT_FILE = os.path.join(INPUTS_DIR, "input04.txt")

BOARD_SIZE = 5


def has_bingo(board: Board) -> bool:
    for row in board:
        if all(x is None for x in row):
            return True
    for col in range(BOARD_SIZE):
        if all(row[col] is None for row in board):
            return True
    # diagonals don't count
    return False


def mark_number(board: Board, num: int) -> bool:
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == num:
                board[i][j] = None
                return True
    return False


if __name__ == "__main__":
    boards = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        numbers = list(map(int, f.readline().strip().split(",")))
        while True:
            line = f.readline()  # skip the blank line
            if line == "":
                break
            b = list()
            for _ in range(BOARD_SIZE):
                row_ = list(map(int, f.readline().strip().split()))
                b.append(row_)
            boards.append(b)
    # simulate bingo
    winning_board = None
    winning_number_index = None
    for i, number in enumerate(numbers):
        for b in boards:
            found = mark_number(b, number)
            if found and has_bingo(b):
                # winner!
                winning_board = b
                winning_number_index = i
                break
        if winning_board is not None:
            break
    else:
        raise ValueError("No winner was found")
    total_sum = sum(sum(val for val in row if val is not None) for row in winning_board)
    winning_number = numbers[winning_number_index]
    score = total_sum * winning_number
    print(f"SCORE: {score}")
