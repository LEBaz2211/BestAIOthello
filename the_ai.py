import numpy as np
from easyAI import TwoPlayerGame,Human_Player, AI_Player, Negamax

to_string = lambda a: "ABCDEFGH"[a[0]] + str(a[1] + 1)
to_array = lambda s: np.array(["ABCDEFGH".index(s[0]), int(s[1]) - 1])


class OthelloAI(TwoPlayerGame):

    def __init__(self, players, state, board=None):
        self.players = players
        self.state = state
        self.board = self.state_to_board()
        self.current_player = (state["current"] + 1)


    def state_to_board(self):
        pass
        

    def possible_moves(self):
        pos_moves = [
            to_string((i, j))
            for i in range(8)
            for j in range(8)
            if (self.board[i, j] == 0)
            and (pieces_flipped(self.board, (i, j), self.current_player) != [])
        ]
        return pos_moves

    def make_move(self, pos):
        pass

    def is_over(self):
        return self.possible_moves() == []

    def scoring(self):
        if np.sum(self.board == 0) > 32:  # less than half the board is full
            player = (self.board == self.current_player).astype(int)
            opponent = (self.board == self.opponent_index).astype(int)
            return ((player - opponent) * BOARD_SCORE).sum()
        else:
            npieces_player = np.sum(self.board == self.current_player)
            npieces_opponent = np.sum(self.board == self.opponent_index)
            return npieces_player - npieces_opponent


# This board is used by the AI to give more importance to the border
BOARD_SCORE = np.array(
    [
        [9, 3, 3, 3, 3, 3, 3, 9],
        [3, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 3],
        [9, 3, 3, 3, 3, 3, 3, 9],
    ]
)

DIRECTIONS = [
    np.array([i, j]) for i in [-1, 0, 1] for j in [-1, 0, 1] if (i != 0 or j != 0)
]
