import unittest

from game.board import Board
from game.player import Player
from utils.consts import BOARD_PAWN_DIM, BOARD_WALL_DIM, DOWN, UP, HORIZONTAL, LEFT, RIGHT, VERTICAL

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

        # it should not be possible to put another wall on the same coordinates
        with self.assertRaises(Exception):
            board.useWall(x, y, HORIZONTAL)
        with self.assertRaises(Exception):
            board.useWall(x, y, VERTICAL)
        # horizontal walls should not be allowed near it ( from left-right perspective), but vertical ones should
        # wall on the left:
        # horizontal
        ynear = y - 1
        with self.assertRaises(Exception):
            board.useWall(x, ynear, HORIZONTAL)
        # vertical
        try:
            board.useWall(x, ynear, VERTICAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        # wall on the right:
        # horizontal
        ynear = y + 1
        with self.assertRaises(Exception):
            board.useWall(x, ynear, HORIZONTAL)
        # vertical
        try:
            board.useWall(x, ynear, VERTICAL)
        except:
            self.fail("This position of a wall should not have thrown errors!")

        # need a new board, because we cannot delete walls from it
        board = Board(Player(), Player())
        # testing for vertical walls
        x = BOARD_WALL_DIM // 2
        y = BOARD_WALL_DIM // 2
        try:
            board.useWall(x, y, VERTICAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        # it should not be possible to put another wall on the same coordinates
        with self.assertRaises(Exception):
            board.useWall(x, y, HORIZONTAL)
        with self.assertRaises(Exception):
            board.useWall(x, y, VERTICAL)
        # vertical walls should not be allowed near it ( from up-down perspective), but horizontal ones should
        # down wall:
        # vertical
        xnear = x - 1
        with self.assertRaises(Exception):
            board.useWall(xnear, y, VERTICAL)
        # horizontal
        try:
            board.useWall(xnear, y, HORIZONTAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        # up wall:
        # vertical
        xnear = x + 1
        with self.assertRaises(Exception):
            board.useWall(xnear, y, VERTICAL)
        # horizontal
        try:
            board.useWall(xnear, y, HORIZONTAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        # validate walls out of boundaries
        
        with self.assertRaises(Exception):
            board.useWall(BOARD_WALL_DIM, BOARD_WALL_DIM - 1, HORIZONTAL)
        with self.assertRaises(Exception):
            board.useWall(-1, BOARD_WALL_DIM - 1, HORIZONTAL)
        with self.assertRaises(Exception):
            board.useWall(BOARD_WALL_DIM - 1, BOARD_WALL_DIM, HORIZONTAL)
        with self.assertRaises(Exception):
            board.useWall(BOARD_WALL_DIM - 1, -1, HORIZONTAL)
        
        # validate for the "funny" guys
        with self.assertRaises(Exception):
            board.useWall(BOARD_WALL_DIM - 1, 0, "funny constant")

    def test_moves_wo_walls_position_board(self):
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

    def test_moves_with_walls_position_board(self):
        # start position:
        # human: 0 4
        # ai: 8 4
        player1 = Player(True)
        player2 = Player(False)
        board = Board(player1, player2)
        # validate coordinates
        self.assertTrue(BoardTest.validate_coordinates(board, 0, 4, 8, 4))

        x = BOARD_PAWN_DIM // 2
        y = BOARD_PAWN_DIM // 2

        player1.x = x
        player1.y = y

        # FIRST CASE
        # test wall that blocks UP move
        try:
            board.useWall(x - 1, y - 1, HORIZONTAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        self.assertFalse(board.validateSimpleMove(UP, [x, y], player2))
        self.assertTrue(board.validateSimpleMove(DOWN, [x, y], player2))
        self.assertTrue(board.validateSimpleMove(LEFT, [x, y], player2))
        self.assertTrue(board.validateSimpleMove(RIGHT, [x, y], player2))
        
        # test wall that blocks DOWN move
        try:
            board.useWall(x, y, HORIZONTAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        self.assertFalse(board.validateSimpleMove(UP, [x, y], player2))
        self.assertFalse(board.validateSimpleMove(DOWN, [x, y], player2))
        self.assertTrue(board.validateSimpleMove(LEFT, [x, y], player2))
        self.assertTrue(board.validateSimpleMove(RIGHT, [x, y], player2))
        
        # test wall that blocks LEFT move
        try:
            board.useWall(x, y - 1, VERTICAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        self.assertFalse(board.validateSimpleMove(UP, [x, y], player2))
        self.assertFalse(board.validateSimpleMove(DOWN, [x, y], player2))
        self.assertFalse(board.validateSimpleMove(LEFT, [x, y], player2))
        self.assertTrue(board.validateSimpleMove(RIGHT, [x, y], player2))

        # test wall that blocks RIGHT move
        try:
            board.useWall(x - 1, y, VERTICAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        self.assertFalse(board.validateSimpleMove(UP, [x, y], player2))
        self.assertFalse(board.validateSimpleMove(DOWN, [x, y], player2))
        self.assertFalse(board.validateSimpleMove(LEFT, [x, y], player2))
        self.assertFalse(board.validateSimpleMove(RIGHT, [x, y], player2))

        # SECOND CASE

        board = Board(player1, player2)
        
        # test wall that blocks UP move
        try:
            board.useWall(x - 1, y, HORIZONTAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        self.assertFalse(board.validateSimpleMove(UP, [x, y], player2))
        self.assertTrue(board.validateSimpleMove(DOWN, [x, y], player2))
        self.assertTrue(board.validateSimpleMove(LEFT, [x, y], player2))
        self.assertTrue(board.validateSimpleMove(RIGHT, [x, y], player2))
        
        # test wall that blocks DOWN move
        try:
            board.useWall(x, y - 1, HORIZONTAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        self.assertFalse(board.validateSimpleMove(UP, [x, y], player2))
        self.assertFalse(board.validateSimpleMove(DOWN, [x, y], player2))
        self.assertTrue(board.validateSimpleMove(LEFT, [x, y], player2))
        self.assertTrue(board.validateSimpleMove(RIGHT, [x, y], player2))
        
        # test wall that blocks LEFT move
        try:
            board.useWall(x - 1, y - 1, VERTICAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        self.assertFalse(board.validateSimpleMove(UP, [x, y], player2))
        self.assertFalse(board.validateSimpleMove(DOWN, [x, y], player2))
        self.assertFalse(board.validateSimpleMove(LEFT, [x, y], player2))
        self.assertTrue(board.validateSimpleMove(RIGHT, [x, y], player2))

        # test wall that blocks RIGHT move
        try:
            board.useWall(x, y, VERTICAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")

        self.assertFalse(board.validateSimpleMove(UP, [x, y], player2))
        self.assertFalse(board.validateSimpleMove(DOWN, [x, y], player2))
        self.assertFalse(board.validateSimpleMove(LEFT, [x, y], player2))
        self.assertFalse(board.validateSimpleMove(RIGHT, [x, y], player2))

    def test_moves_validation(self):
        # TODO
        None

    def test_get_all_actions(self):
        # Reminder:
        # exclude tests that may give special moves
        
        # human: 0 4
        # ai: 8 4
        player1 = Player(True)
        player2 = Player(False)
        board = Board(player1, player2)
        # validate coordinates
        self.assertTrue(BoardTest.validate_coordinates(board, 0, 4, 8, 4))

        # validations only for 0 walls ( simpler ones)
        player1.no_walls = 0

        player1.x = 0
        player1.y = BOARD_PAWN_DIM // 2

        # validate boundaries with corners as well
        # UP should not be allowed
        self.assertListEqual([DOWN, LEFT, RIGHT], board.getAllActionsForAPlayer(player1, player2))

        player1.x = BOARD_PAWN_DIM - 1

        # DOWN should not be allowed
        self.assertListEqual([UP, LEFT, RIGHT], board.getAllActionsForAPlayer(player1, player2))

        player1.x = BOARD_PAWN_DIM // 2
        player1.y = 0

        # LEFT should not be allowed
        self.assertListEqual([UP, DOWN, RIGHT], board.getAllActionsForAPlayer(player1, player2))

        player1.y = BOARD_PAWN_DIM - 1

        # RIGHT should not be allowed
        self.assertListEqual([UP, DOWN, LEFT], board.getAllActionsForAPlayer(player1, player2))

        player1.x = 0

        # UP AND RIGHT should not be allowed
        self.assertListEqual([DOWN, LEFT], board.getAllActionsForAPlayer(player1, player2))

        player1.x = BOARD_PAWN_DIM - 1

        # DOWN AND RIGHT should not be allowed
        self.assertListEqual([UP, LEFT], board.getAllActionsForAPlayer(player1, player2))
        
        player1.x = 0
        player1.y = 0

        # UP AND LEFT should not be allowed
        self.assertListEqual([DOWN, RIGHT], board.getAllActionsForAPlayer(player1, player2))

        player1.x = BOARD_PAWN_DIM - 1

        # DOWN AND LEFT should not be allowed
        self.assertListEqual([UP, RIGHT], board.getAllActionsForAPlayer(player1, player2))

        player1.x = BOARD_PAWN_DIM // 2
        player1.y = BOARD_PAWN_DIM // 2

        # all moves should be allowed
        self.assertListEqual([UP, DOWN, LEFT, RIGHT], board.getAllActionsForAPlayer(player1, player2))
        x = BOARD_PAWN_DIM // 2
        y = BOARD_PAWN_DIM // 2
        # validate moves with walls
        try:
            board.useWall(x - 1, y - 1, HORIZONTAL)
            board.useWall(x - 1, y, VERTICAL)
            board.useWall(x, y - 1, VERTICAL)
            board.useWall(x, y, HORIZONTAL)
        except:
            self.fail("The position of this wall should not have thrown errors!")
        
        self.assertListEqual([], board.getAllActionsForAPlayer(player1, player2))

        # reset the board ( we do not want walls anywhere)
        board = Board(player1, player2)
        # reset the walls of the first player
        player1.no_walls = 10
        walls = []
        for i in range(BOARD_WALL_DIM):
            for j in range(BOARD_WALL_DIM):
                walls.append((i, j, HORIZONTAL))
                walls.append((i, j, VERTICAL))
        
        self.assertListEqual(walls + [UP, DOWN, LEFT, RIGHT], board.getAllActionsForAPlayer(player1, player2))

        # TODO
        # tests that may give special moves
