import unittest
from easyAI import Negamax, AI_Player
from the_ai import OthelloAI, pieces_flipped, move_extractor
import numpy as np
from copy import deepcopy


class TestOthelloAI(unittest.TestCase):

    def setUp(self):
        self.board = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,2,1,0,0,0],
            [0,0,0,1,2,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]]
        self.board1 = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0],
            [0,0,0,1,1,0,0,0],
            [0,0,0,1,2,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]]
        self.state = {'players': ['OmegaZero', 'OmegaZero1'], 'current': 0, 'board': [[28, 35], [27, 36]]}
        ai = Negamax(1)
        self.the_game = OthelloAI([AI_Player(ai), AI_Player(ai)], self.state)

    def tearDown(self):
        pass

    def test_state_to_board(self):
        self.assertEqual(self.the_game.state_to_board().tolist(), [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,2,1,0,0,0],
            [0,0,0,1,2,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]])

    def test_possible_moves(self):
        self.assertEqual(self.the_game.possible_moves(), ['C4', 'D3', 'E6', 'F5'])

    def test_make_move(self):
        self.the_game.make_move('C4')
        for i in range(8):
            for j in range(8):

                self.assertEqual(self.the_game.board[i][j], self.board1[i][j])

    def test_is_over(self):
        self.assertEqual(self.the_game.is_over(), False)

    def test_scoring(self):
        self.assertEqual(self.the_game.scoring(), 0)
        best_move = self.the_game.get_move()
        self.the_game.make_move(best_move)
        self.assertEqual(self.the_game.scoring(), 8)

    def test_pieces_flipped(self):
        self.assertEqual(pieces_flipped(self.board, (5, 4), 1)[0].tolist(), [4,4])
        self.assertEqual(pieces_flipped(self.board, (5, 6), 1), [])

    def test_move_extractor(self):
        self.assertEqual(move_extractor(self.state), 19)

if __name__ == "__main__":
    unittest.main()