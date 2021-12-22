import os
import re
from copy import copy

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input21.txt")
INPUT_RE = re.compile(r"Player [12] starting position: (\d+)")

WINNING_SCORE_DETERMINISTIC = 1000
WINNING_SCORE_DIRAC = 21
N_ROLLS_PER_TURN = 3
POS_FIRST = 1
POS_LAST = 10
BOARD_SIZE = 1 + POS_LAST - POS_FIRST
DIE_DIRAC = [1, 2, 3]


class DeterministicDie:
    def __init__(self, low: int = 1, high: int = 100):
        self.low = low
        self.high = high
        self.prev_value = low - 1
        self.n_rolls = 0

    def roll(self) -> int:
        self.n_rolls += 1
        if self.prev_value == self.high:
            self.prev_value = self.low
        else:
            self.prev_value += 1
        return self.prev_value


class Player:
    def __init__(self, player_id: int, start_position: int):
        self.player_id = player_id
        self.pos = start_position
        self.score = 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.player_id}, pos={self.pos}, score={self.score})"

    def take_turn(self, die: DeterministicDie) -> bool:
        # how many to move
        total = 0
        for _ in range(N_ROLLS_PER_TURN):
            total += die.roll()
        # move that many
        self.pos += total
        while self.pos > POS_LAST:  # circular board
            self.pos -= BOARD_SIZE
        # score goes up according to the number you landed on
        self.score += self.pos
        # did we win?
        return self.score >= WINNING_SCORE_DETERMINISTIC


# part 2
class DiracGame:
    def __init__(self, p1_id: int = 1, p2_id: int = 2):
        self.p1_id = p1_id
        self.p2_id = p2_id
        self.p1_wins = 0
        self.p2_wins = 0

    def _play_dfs(self, player_current: Player, player_other: Player, n_rolls_used: int, this_turn_sum: int):
        # are we at the end of a turn?
        if n_rolls_used == N_ROLLS_PER_TURN:
            # don't edit the instances that previous stack frames are using
            player_current = copy(player_current)
            # actually do the move
            player_current.pos += this_turn_sum
            while player_current.pos > POS_LAST:  # circular board
                player_current.pos -= BOARD_SIZE
            # score goes up according to the number you landed on
            player_current.score += player_current.pos
            # did we win?
            if player_current.score >= WINNING_SCORE_DIRAC:  # yes
                # which player was it? give them the point
                if player_current.player_id == self.p1_id:
                    self.p1_wins += 1
                else:
                    self.p2_wins += 1
            else:  # no
                # game still going; now it's the other player's turn
                self._play_dfs(player_other, player_current, 0, 0)
        else:
            # do another roll; try all the options
            for roll_value in DIE_DIRAC:
                self._play_dfs(player_current, player_other, n_rolls_used + 1, this_turn_sum + roll_value)

    def play_all(self, p1_pos: int, p2_pos: int):
        self.p1_wins = 0
        self.p2_wins = 0
        self._play_dfs(Player(self.p1_id, p1_pos), Player(self.p2_id, p2_pos), 0, 0)


if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        p1_pos_ = int(INPUT_RE.fullmatch(f.readline().strip()).group(1))
        p2_pos_ = int(INPUT_RE.fullmatch(f.readline().strip()).group(1))
    p1_ = Player(1, p1_pos_)
    p2_ = Player(2, p2_pos_)
    die_ = DeterministicDie()
    player_next_, player_other_ = p1_, p2_
    while True:  # play until we have a winner
        finished_ = player_next_.take_turn(die_)
        if finished_:
            break
        player_next_, player_other_ = player_other_, player_next_
    # player_next is winner, player_other is loser
    prod = player_other_.score * die_.n_rolls
    print(f"PRODUCT of loser's score and number of rolls: {prod}")
    print("-----")
    # part 2
    game = DiracGame()
    game.play_all(p1_pos_, p2_pos_)
    most_wins = max(game.p1_wins, game.p2_wins)
    print(f"MOST wins for one player: {most_wins}")
