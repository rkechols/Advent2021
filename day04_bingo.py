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


def get_score(board: Board, num: int) -> int:
    total_sum = sum(sum(val for val in row if val is not None) for row in board)
    score = total_sum * num
    return score


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
    found_first = False
    loser_board = None
    for number in numbers:
        next_boards = list()
        for b in boards:
            found = mark_number(b, number)
            if found and has_bingo(b):
                # winner!
                if not found_first:
                    found_first = True
                    score_ = get_score(b, number)
                    print(f"SCORE of first winner: {score_}")
                if b is loser_board:  # check identity; is this winner the last board playing?
                    score_ = get_score(loser_board, number)
                    print(f"SCORE of last winner: {score_}")
                    exit(0)
                # a winner doesn't get added to `next_boards`
            else:  # not a winner; keep it for the next time
                next_boards.append(b)
        boards = next_boards
        if len(boards) == 1:  # last board playing is the loser; save it
            loser_board = boards[0]
        elif len(boards) == 0:
            raise ValueError("there was no single losing board (i.e. there was a tie for last)")
