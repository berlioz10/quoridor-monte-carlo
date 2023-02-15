import unittest

from game.board import Board
from game.player import Player
from utils.consts import BOARD_PAWN_DIM, BOARD_WALL_DIM, DOWN, UP, HORIZONTAL, LEFT, RIGHT

class BoardTest(unittest.TestCase):
    def validate_coordinates(board: Board, player1x: int, player1y: int, player2x: int, player2y: int) -> bool:
        if board.player1.x != player1x:
            return False
        if board.player1.y != player1y:
            return False
        if board.player2.x != player2x:
            return False
        if board.player2.y != player2y:
            return False
        
        return True

    def test_initialize_board(self):
        # start position:
        # human: 0 4
        # ai: 8 4
        player1 = Player(True)
        player2 = Player(False)
        board = Board(player1, player2)
        self.assertEqual(board.player1, player1)
        self.assertEqual(board.player2, player2)
    
    def test_putting_walls(self):
        # we do not need players for this tests
        board = Board(Player(), Player())
        # testing for horizontal walls
        x = BOARD_WALL_DIM // 2
        y = BOARD_WALL_DIM // 2
        try:
            board.useWall(x, y, HORIZONTAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        # horizontal walls should not be allowed near it, but vertical ones should

    def test_wo_walls_position_board(self):
        # start position:
        # human: 0 4
        # ai: 8 4
        player1 = Player(True)
        player2 = Player(False)
        board = Board(player1, player2)
        # validate coordinates
        self.assertTrue(BoardTest.validate_coordinates(board, 0, 4, 8, 4))

        player2.x = BOARD_PAWN_DIM // 2
        player2.y = BOARD_PAWN_DIM // 2

        # player1 is located like this:
        # -----
        # . X .
        # . . .
        # UP move should be false
        self.assertTrue(board.validateSimpleMove(LEFT, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(RIGHT, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(DOWN, [player1.x, player1.y], player2))
        self.assertFalse(board.validateSimpleMove(UP, [player1.x, player1.y], player2))

        player1.x = BOARD_PAWN_DIM // 2
        player1.y = 0

        # player1 is located like this:
        # - . .
        # - X .
        # - . .
        # LEFT move should be false
        self.assertTrue(board.validateSimpleMove(DOWN, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(RIGHT, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(UP, [player1.x, player1.y], player2))
        self.assertFalse(board.validateSimpleMove(LEFT, [player1.x, player1.y], player2))

        player1.y = BOARD_PAWN_DIM - 1

        # player1 is located like this:
        # . . -
        # . X -
        # . . -
        # RIGHT move should be false
        self.assertTrue(board.validateSimpleMove(LEFT, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(UP, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(DOWN, [player1.x, player1.y], player2))
        self.assertFalse(board.validateSimpleMove(RIGHT, [player1.x, player1.y], player2))

        player1.x = BOARD_PAWN_DIM - 1
        player1.y = BOARD_PAWN_DIM // 2
        # player1 is located like this:
        # . . .
        # . X .
        # -----
        # DOWN move should be false
        self.assertTrue(board.validateSimpleMove(LEFT, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(RIGHT, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(UP, [player1.x, player1.y], player2))
        self.assertFalse(board.validateSimpleMove(DOWN, [player1.x, player1.y], player2))

        player1.x = 0
        player1.y = BOARD_PAWN_DIM - 1
        # player1 is located like this:
        # -----
        # . X -
        # . . -
        # UP and RIGHT move should be false
        self.assertTrue(board.validateSimpleMove(LEFT, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(DOWN, [player1.x, player1.y], player2))
        self.assertFalse(board.validateSimpleMove(RIGHT, [player1.x, player1.y], player2))
        self.assertFalse(board.validateSimpleMove(UP, [player1.x, player1.y], player2))

        player1.x = 0
        player1.y = 0
        # player1 is located like this:
        # -----
        # - X .
        # - . .
        # UP and LEFT move should be false
        self.assertTrue(board.validateSimpleMove(DOWN, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(RIGHT, [player1.x, player1.y], player2))
        self.assertFalse(board.validateSimpleMove(LEFT, [player1.x, player1.y], player2))
        self.assertFalse(board.validateSimpleMove(UP, [player1.x, player1.y], player2))

        player1.x = BOARD_PAWN_DIM - 1
        player1.y = 0
        # player1 is located like this:
        # - . .
        # - X .
        # -----
        # DOWN and LEFT move should be false
        self.assertTrue(board.validateSimpleMove(UP, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(RIGHT, [player1.x, player1.y], player2))
        self.assertFalse(board.validateSimpleMove(DOWN, [player1.x, player1.y], player2))
        self.assertFalse(board.validateSimpleMove(LEFT, [player1.x, player1.y], player2))

        player1.x = BOARD_PAWN_DIM - 1
        player1.y = BOARD_PAWN_DIM - 1
        # player1 is located like this:
        # . . -
        # . X -
        # -----
        # RIGHT and DOWN move should be false
        self.assertTrue(board.validateSimpleMove(UP, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(LEFT, [player1.x, player1.y], player2))
        self.assertFalse(board.validateSimpleMove(DOWN, [player1.x, player1.y], player2))
        self.assertFalse(board.validateSimpleMove(RIGHT, [player1.x, player1.y], player2))
        
        player1.x = BOARD_PAWN_DIM // 2
        player1.y = BOARD_PAWN_DIM // 2
        # player1 is located like this:
        # . . .
        # . X .
        # . . .
        # None should be false
        self.assertTrue(board.validateSimpleMove(UP, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(LEFT, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(DOWN, [player1.x, player1.y], player2))
        self.assertTrue(board.validateSimpleMove(RIGHT, [player1.x, player1.y], player2))

        player2.x = player1.x
        player2.y = player1.y + 1
        # player1 with player2 is located like this:
        # . . .
        # . X Y
        # . . .
        # RIGHT should be false
        self.assertFalse(board.validateSimpleMove(RIGHT, [player1.x, player1.y], player2))
        
        player2.y = player1.y - 1
        # player1 with player2 is located like this:
        # . . .
        # Y X .
        # . . .
        # LEFT should be false
        self.assertFalse(board.validateSimpleMove(LEFT, [player1.x, player1.y], player2))

        player2.x = player1.x + 1
        player2.y = player1.y
        # player1 with player2 is located like this:
        # . . .
        # . X .
        # . Y .
        # DOWN should be false
        self.assertFalse(board.validateSimpleMove(DOWN, [player1.x, player1.y], player2))

        player2.x = player1.x - 1
        # player1 with player2 is located like this:
        # . Y .
        # . X .
        # . . .
        # UP should be false
        self.assertFalse(board.validateSimpleMove(UP, [player1.x, player1.y], player2))

    def test_with_walls_position_board(self):
        # start position:
        # human: 0 4
        # ai: 8 4
        player1 = Player(True)
        player2 = Player(False)
        board = Board(player1, player2)
        # validate coordinates
        self.assertTrue(BoardTest.validate_coordinates(board, 0, 4, 8, 4))

        player2.x = BOARD_PAWN_DIM // 2
        player2.y = BOARD_PAWN_DIM // 2
