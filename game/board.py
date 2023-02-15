import copy
from game.player import Player
from utils.consts import BOARD_PAWN_DIM, BOARD_WALL_DIM, DOWN, HORIZONTAL, LEFT, RIGHT, UP, VERTICAL

class Board:
    def __init__(self, player1: Player, player2: Player):
        self.wallsAllowed = []
        self.wallsUsed = []
        self.leftRight = []
        self.upDown = []
        
        for _ in range(BOARD_WALL_DIM):
            self.wallsAllowed.append({HORIZONTAL: [True for _ in range(BOARD_WALL_DIM)], VERTICAL: [True for _ in range(BOARD_WALL_DIM)]})
            self.wallsUsed.append(["" for _ in range(BOARD_WALL_DIM)])

        # left-right
        # for _ in range(BOARD_PAWN_DIM):
        #    self.leftRight.append([True for _ in range(BOARD_WALL_DIM)]) 

        # up-down
        # for _ in range(BOARD_WALL_DIM):
        #    self.leftRight.append([True for _ in range(BOARD_PAWN_DIM)])

        self.player1 = player1
        self.player2  = player2

    def getAllActionsForAPlayer(self, playerMove: Player, otherPlayer: Player):
        actions_list = []
        
        # walls allowed ( only if the player has anymore walls to use)
        if playerMove.walls != 0:
            for i in range(BOARD_WALL_DIM):
                for j in range(BOARD_WALL_DIM):
                    if self.wallsAllowed[i][HORIZONTAL][j] == True:
                        actions_list.append((i, j, HORIZONTAL))
                    if self.wallsAllowed[i][VERTICAL][j] == True:
                        actions_list.append((i, j, VERTICAL))
        
        # the moves the player which moves is allowed ( without considering the other player, only as a "wall")

        pos = [playerMove.x, playerMove.y]

        if self.validateSimpleMove(UP, pos, otherPlayer):
            actions_list.append(UP)
        
        if self.validateSimpleMove(DOWN, pos, otherPlayer):
            actions_list.append(DOWN)

        if self.validateSimpleMove(LEFT, pos, otherPlayer):
            actions_list.append(LEFT)

        if self.validateSimpleMove(RIGHT, pos, otherPlayer):
            actions_list.append(RIGHT)

        # validate special moves ( the ones that are near another pawn or smth like that)
        # TODO 

        return actions_list

    # tries to put a wall in the board
    # validates if it is out of boundaries, consts are incorrect and etc.
    # if the validation process is ok, then places a wall
    # and sets the allowance of other walls near it
    # x, y - numbers, coordinates of the wall
    # position - VERTICAL or HORIZONTAL ( consts), how the wall should be put
    def useWall(self, x: int, y: int, position: str):
        if x < 0 or x > BOARD_WALL_DIM - 1 or y < 0 or y > BOARD_WALL_DIM - 1:
            raise Exception("Coordinates of the wall are not between 0 and 7") 
        if position != HORIZONTAL and position != VERTICAL:
            raise Exception("Not a possible position: only HORIZONTAL or VERTICAL")

        if self.wallsAllowed[x][position][y] == False:
            raise Exception("Wall is not allowed")

        self.wallsAllowed[x][HORIZONTAL][y] = False
        self.wallsAllowed[x][VERTICAL][y] = False
        self.wallsUsed[x][y] = position

        if position == HORIZONTAL:
            if y > 0:
                self.wallsAllowed[x][HORIZONTAL][y - 1] = False
                
            
            if y < BOARD_WALL_DIM - 1:
                self.wallsAllowed[x][HORIZONTAL][y + 1] = False 
        
        
        if position == VERTICAL:
            if x > 0:
                self.wallsAllowed[x - 1][VERTICAL][y] = False
            
            if x < BOARD_WALL_DIM - 1:
                self.wallsAllowed[x + 1][VERTICAL][y] = False
        
    # validates if a move from coordinates ( which are given as a list)
    # can actually make that move
    # this is a simple version, as in it does not interfere with special actions with another player
    # ( like jumping him etc.)
    # mov - UP DOWN LEFT RIGHT ( consts), and nothing more
    # pos - a list of length 2, with 2 numbers that should be between 0 and BOARD_PAWN_DIM ( an integer const)
    # otherPlayer - the other player ( we need him because he should not make moves that will make 
    # the two pawns have the same coordinates)

    # # TODO: the validation of this function is not as strict as the "useWall" method:
    # it does not validate if pos has enough values, or if the move is valid
    def validateSimpleMove(self, move: str, pos: list, otherPlayer: Player) -> bool:
        if len(pos) != 2:
            raise Exception("Pos list must have the length of 2 ( coordinates x and y)")
        x = pos[0]
        y = pos[1]
        if move == UP:
            if x == 0 or (x - 1 == otherPlayer.x and y == otherPlayer.y):
                return False
            row = self.wallsUsed[x - 1]
            if y == 0:
                if row[0] == HORIZONTAL:
                    return False
            elif y == BOARD_PAWN_DIM - 1:
                if row[BOARD_WALL_DIM - 1] == HORIZONTAL:
                    return False
            elif row[y] == HORIZONTAL or row[y - 1] == HORIZONTAL:
                return False

        elif move == DOWN:
            if x == BOARD_PAWN_DIM - 1 or (x + 1 == otherPlayer.x and y == otherPlayer.y):
                return False
            row = self.wallsUsed[x]
            if y == 0:
                if row[0] == HORIZONTAL:
                    return False
            elif y == BOARD_PAWN_DIM - 1:
                if row[BOARD_WALL_DIM - 1] == HORIZONTAL:
                    return False
            elif row[y] == HORIZONTAL or row[y - 1] == HORIZONTAL:
                return False

        elif move == LEFT:
            if y == 0 or (x == otherPlayer.x and y - 1 == otherPlayer.y):
                return False
            column_index = y - 1
            if x == 0:
                if self.wallsUsed[x][column_index] == VERTICAL:
                    return False
            elif x == BOARD_PAWN_DIM - 1:
                if self.wallsUsed[BOARD_WALL_DIM - 1][column_index] == VERTICAL:
                    return False
            elif self.wallsUsed[x][column_index] == VERTICAL or self.wallsUsed[x - 1][column_index] == VERTICAL:
                return False

        elif move == RIGHT:
            if y == BOARD_PAWN_DIM - 1 or (x == otherPlayer.x and y + 1 == otherPlayer.y):
                return False
            column_index = y
            if x == 0:
                if self.wallsUsed[x][column_index] == VERTICAL:
                    return False
            elif x == BOARD_PAWN_DIM - 1:
                if self.wallsUsed[BOARD_WALL_DIM - 1][column_index] == VERTICAL:
                    return False
            elif self.wallsUsed[x][column_index] == VERTICAL or self.wallsUsed[x - 1][column_index] == VERTICAL:
                return False

        return True

    def shortestMove(self, player: Player, otherPlayer: Player, winningRow: int) -> int:
        # calculate the shortest path to the end
        lee = [[0 for _ in range(BOARD_PAWN_DIM)] for _ in range(BOARD_PAWN_DIM)]

        moves = { DOWN: [1, 0], UP: [-1, 0], RIGHT: [0, 1], LEFT: [0, -1]}

        q = [[player.x, player.y]]

        lee[q[0], q[1]] = 1
        while len(q) != 0:
            pos = q.pop(0)
            for move in moves.keys():
                x = pos[0] + moves[move][0]
                y = pos[1] + moves[move][1]
                if self.validateSimpleMove(move, pos, otherPlayer):
                    if lee[pos[0]][pos[1]] + 1 < lee[x][y] or lee[x][y] == 0:
                        lee[x][y] = lee[pos[0]][pos[1]] + 1  
                        q.append([x, y])

        min_values = [x for x in lee[winningRow] if x != 0]

        if len(min_values) == 0:
            raise Exception("Impossible to finish")
        
        ct = min(min_values)

        return ct

    def deepCopy(self, player1: Player, player2: Player) -> 'Board':
        board = Board(player1, player2)
        board.wallsAllowed = copy.deepcopy(self.wallsAllowed)
        board.wallsUsed = copy.deepcopy(self.wallsUsed)

        return board