import numpy as np
from easyAI import TwoPlayerGame, AI_Player, Negamax

to_string = lambda a: "ABCDEFGH"[a[0]] + str(a[1] + 1)
to_array = lambda s: np.array(["ABCDEFGH".index(s[0]), int(s[1]) - 1])


class OthelloAI(TwoPlayerGame):
    """The OthelloAI class is used to define and implement the algorithm"""

    def __init__(self, players, state, board=None):
        """Initialisation of the game"""

        self.players = players
        self.state = state
        self.board = self.state_to_board()
        self.current_player = (state["current"] + 1)


    def state_to_board(self):
        """Updates the dtate of the board"""
        board = np.zeros((8, 8), dtype=int)
        for case in self.state["board"][0]:
            board[case//8][(case%8)] = 1
        for case in self.state["board"][1]:
            board[case//8][(case%8)] = 2
        return(board)
        

    def possible_moves(self):
        """This function returns all the possible moves that AI can play"""
        pos_moves = [
            to_string((i, j))
            for i in range(8)
            for j in range(8)
            if (self.board[i, j] == 0)
            and (pieces_flipped(self.board, (i, j), self.current_player) != [])
        ]
        return pos_moves

    def make_move(self, pos):
        """Transforms the game according to the moves"""
        pos = to_array(pos)
        flipped = pieces_flipped(self.board, pos, self.current_player)
        for i, j in flipped:
            self.board[i, j] = self.current_player
        self.board[pos[0], pos[1]] = self.current_player      

    def is_over(self):
        """Checks if the game has ended"""
        return self.possible_moves() == []

    def scoring(self):
        """Gives a score to the current game (for the AI), to aim for the higher score we give higher values to more strategic positions"""
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

def pieces_flipped(board, pos, current_player):
    """It dertermines which pawns have been taken and need to be flipped (to change color)"""
    flipped = []

    for d in DIRECTIONS:
        ppos = pos + d
        streak = []
        while (0 <= ppos[0] <= 7) and (0 <= ppos[1] <= 7):
            if board[ppos[0], ppos[1]] == 3 - current_player:
                streak.append(+ppos)
            elif board[ppos[0], ppos[1]] == current_player:
                flipped += streak
                break
            else:
                break
            ppos += d

    return flipped

def move_extractor(state) :
    """It is defined to more efficiently run the game and give the necessary argguments to the algorithm"""
    rec = 4
    ai = Negamax(rec)
    the_game = OthelloAI([AI_Player(ai), AI_Player(ai)], state)
    try :
        the_move = the_game.get_move()
        list1 = ("A,B,C,D,E,F,G,H").split(",")
        real_move = 0
        for i in the_move :
            if i in list1 :
                real_move +=((list1.index(i))*8)
            else :
                real_move += (int(i)-1)
            return (real_move)
    except :
        print("No possible moves left")
