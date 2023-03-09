from utils.consts import BOARD_PAWN_DIM, DOWN, DOWN_DOWN, DOWN_LEFT, DOWN_RIGHT, LEFT, LEFT_LEFT, NO_WALLS, RIGHT, RIGHT_RIGHT, UP, UP_LEFT, UP_RIGHT, UP_UP

class Player:
    def __init__(self, human : bool = True):
        self.y : int = BOARD_PAWN_DIM // 2
        self.x : int = BOARD_PAWN_DIM - 1
        if human:
            self.x = 0

        self.human = human

        self.no_walls : int = NO_WALLS

    def decrementWalls(self):
        self.no_walls -= 1

    def getCoordinates(self):
        return self.x, self.y

    def playMove(self, move: str):
        if move == UP:
            if self.x == 0:
                raise Exception("It is already on the first row, cannot go upper!")
            self.x -= 1
        elif move == DOWN:
            if self.x == BOARD_PAWN_DIM - 1:
                raise Exception("It is already on the last row, cannot go lower!")
            self.x += 1
        elif move == LEFT:
            if self.y == 0:
                raise Exception("It is already on the first column, cannot go more to the left!")
            self.y -= 1
        elif move == RIGHT:
            if self.y == BOARD_PAWN_DIM - 1:
                raise Exception("It is already on the last column, cannot go more to the right!")
            self.y += 1
        elif move == UP_RIGHT:
            if self.x == 0:
                raise Exception("It is already on the first row, cannot go upper!")
            self.x -= 1
            if self.y == BOARD_PAWN_DIM - 1:
                raise Exception("It is already on the last column, cannot go more to the right!")
            self.y += 1
        elif move == UP_LEFT:
            if self.x == 0:
                raise Exception("It is already on the first row, cannot go upper!")
            self.x -= 1
            if self.y == 0:
                raise Exception("It is already on the first column, cannot go more to the left!")
            self.y -= 1
        elif move == DOWN_RIGHT:
            if self.x == BOARD_PAWN_DIM - 1:
                raise Exception("It is already on the last row, cannot go lower!")
            self.x += 1
            if self.y == BOARD_PAWN_DIM - 1:
                raise Exception("It is already on the last column, cannot go more to the right!")
            self.y += 1
        elif move == DOWN_LEFT:
            if self.x == BOARD_PAWN_DIM - 1:
                raise Exception("It is already on the last row, cannot go lower!")
            self.x += 1
            if self.y == 0:
                raise Exception("It is already on the first column, cannot go more to the left!")
            self.y -= 1
        elif move == UP_UP:
            if self.x <= 1:
                raise Exception("It is already on the first or second row, cannot go upper!")
            self.x -= 2
        elif move == DOWN_DOWN:
            if self.x >= BOARD_PAWN_DIM - 2:
                raise Exception("It is already on the second last or even last row, cannot go lower!")
            self.x += 2
        elif move == LEFT_LEFT:
            if self.y <= 1:
                raise Exception("It is already on the first or second column, cannot go lower!")
            self.y -= 2
        elif move == RIGHT_RIGHT:
            if self.y >= BOARD_PAWN_DIM - 2:
                raise Exception("It is already on the second last or even last column, cannot go upper!")
            self.y += 2
        

    def isOnOppositeRow(self):
        if self.human:
            if self.x == BOARD_PAWN_DIM - 1:
                return True
        if not self.human:
            if self.x == 0:
                return True
        return False

    
    def deepCopy(self) -> 'Player':
        player : Player = Player(self.human)
        player.x = self.x
        player.y = self.y
        player.no_walls = self.no_walls

        return player