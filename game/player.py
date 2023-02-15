from utils.consts import BOARD_PAWN_DIM, DOWN, LEFT, NO_WALLS, RIGHT, UP

class Player:
    def __init__(self, human : bool = True):
        self.y : int = BOARD_PAWN_DIM // 2
        self.x : int = BOARD_PAWN_DIM - 1
        if human:
            self.x = 0

        self.human = human

        self.walls : int = NO_WALLS

    def decrementWalls(self):
        self.walls -= 1

    def getCoordinates(self):
        return self.x, self.y

    def playMove(self, move: str):
        if move == UP:
            self.x += 1
        elif move == DOWN:
            self.x -= 1
        elif move == RIGHT:
            self.y += 1
        elif move == LEFT:
            self.y -= 1

    def isOnOppositeRow(self):
        if self.human:
            if self.x == BOARD_PAWN_DIM - 1:
                return True
        else:
            if self.x == 0:
                return True
        return False

    
    def deepCopy(self) -> 'Player':
        player : Player = Player()
        player.x = self.x
        player.y = self.y
        player.walls = self.walls

        return player