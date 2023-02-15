import unittest

from game.board import Board
from game.player import Player

class BoardTest(unittest.TestCase):
    def test_simple_board(self):
        # start position:
        # human: 0 4
        # ai: 8 4
        player1 = Player(True)
        player2 = Player(False)
        board = Board(player1, player2)
        self.assertEqual(board.player1, player1)
        self.assertEqual(board.player2, player2)

