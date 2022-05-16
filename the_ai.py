from time import time
import numpy as np
from easyAI import TranspositionTable, TwoPlayerGame, AI_Player, Negamax, Human_Player
import pickle

to_string = lambda a: "ABCDEFGH"[a[0]] + str(a[1] + 1)
to_array = lambda s: np.array(["ABCDEFGH".index(s[0]), int(s[1]) - 1])

class OthelloAI(TwoPlayerGame):
    """
    The OthelloAI class is used to define and implement the algorithm
    """

    def __init__(self, players, state, board=None):
        """
        Initialisation of the game
        """
        self.players = players
        self.state = state
        self.board = self.state_to_board()
        self.current_player = (state["current"] + 1)


    def state_to_board(self):
        """
        Updates the state of the board
        """
        board = np.zeros((8, 8), dtype=int)
        for case in self.state["board"][0]:
            board[case//8][(case%8)] = 1
        for case in self.state["board"][1]:
            board[case//8][(case%8)] = 2
        return(board)

    def possible_moves(self):
        """
        This function returns all the possible moves that AI can play
        """
        poss_moves = [
            to_string((i, j))
            for i in range(8)
            for j in range(8)
            if (self.board[i, j] == 0)
            and (pieces_flipped(self.board, (i, j), self.current_player) != [])
        ]
        return poss_moves

    def make_move(self, pos):
        """
        Transforms the game according to the moves
        """
        pos = to_array(pos)
        flipped = pieces_flipped(self.board, pos, self.current_player)
        for i, j in flipped:
            self.board[i, j] = self.current_player
        self.board[pos[0], pos[1]] = self.current_player    

    def is_over(self):
        """
        Checks if the game has ended
        """
        return self.possible_moves() == []

    def scoring(self):
        """
        Gives a score to the current game (for the AI), to aim for the higher score we give higher values to more strategic positions
        """
        if np.sum(self.board == 0) > 52: #Less than 1/4 of the board is full
            player = (self.board == self.current_player).astype(int)
            opponent = (self.board == self.opponent_index).astype(int)
            return ((player - opponent) * sweat_16).sum() #Rewarded if takes 

        else:
            player = (self.board == self.current_player).astype(int)
            opponent = (self.board == self.opponent_index).astype(int)
            npieces_player = np.sum(self.board == self.current_player)
            npieces_opponent = np.sum(self.board == self.opponent_index)
            return ((player - opponent) * late_game).sum() + (npieces_player - npieces_opponent)
    


sweat_16 = np.array(
    [
        [10, 3, 3, 3, 3, 3, 3, 10],
        [3, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 2, 2, 2, 2, 1, 3],
        [3, 1, 2, 3, 3, 2, 1, 3],
        [3, 1, 2, 3, 3, 2, 1, 3],
        [3, 1, 2, 2, 2, 2, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 3],
        [10, 3, 3, 3, 3, 3, 3, 10]
    ]
)
late_game = np.array(
    [
        [20, 3, 3, 3, 3, 3, 1, 20],
        [1, -1, 1, 1, 1, 1, -1, 1],
        [3, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 3],
        [3, 1, 1, 1, 1, 1, 1, 3],
        [1, -1, 1, 1, 1, 1, -1, 1],
        [20, 1, 3, 3, 3, 3, 1, 20]
    ]
)

dirs = [
    np.array([i, j]) for i in [-1, 0, 1] for j in [-1, 0, 1] if (i != 0 or j != 0)
]

def pieces_flipped(board, pos, current_player):
    """
    Dertermines which pawns have been taken and need to be flipped (to change color)
    """
    flipped = []
    for d in dirs:
        ppos = pos + d
        streak = []
        while (0 <= ppos[0] <= 7) and (0 <= ppos[1] <= 7):
            if board[ppos[0]][ppos[1]] == 3 - current_player:
                streak.append(+ppos)
            elif board[ppos[0]][ppos[1]] == current_player:
                flipped += streak
                break
            else:
                break
            ppos += d
    return flipped




def move_extractor(state) :
    """
    Takes the necessary argguments to the algorithm and returns the move
    """
    rec = 5

    ai = Negamax(rec)

    the_game = OthelloAI([AI_Player(ai), AI_Player(ai)], state)
    try :
        the_move = the_game.get_move()
        [i, j] = to_array(the_move)
        real_move = int((i)*8 + j)
        return real_move
    except :
        print("No possible moves left")



if __name__ == "__main__":

    state = {'players': ['OmegaZero', 'OmegaZero1'], 'current': 0, 'board': [[28, 35], [27, 36]]}

    ai = Negamax(1)

    the_game = OthelloAI([AI_Player(ai), AI_Player(Negamax(1))], state)

    print(the_game.get_move())

    the_game.make_move('C4')