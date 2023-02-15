from game.board import Board
from game.player import Player
from utils.consts import BOARD_PAWN_DIM

class Game:
    # a board
    # players - 2
    # human first turn or not
    def __init__(self, humanFirstTurn : bool = True):
        
        self.humanPlayer : Player = Player(human=True)
        self.AIPlayer : Player = Player(human=False)

        self.board : Board = Board(player1=self.humanPlayer, player2=self.AIPlayer)
        self.humanTurn = humanFirstTurn
        self.gameEnd = False
        self.humanPlayerWon = None

    # TODO: add comment
    def nextMove(self, move: tuple | str):
        try:
            # wall is used
            if type(move) is tuple:
                # adding a new rule for AI:
                self.board.useWall(move[0], move[1], move[2])
                try:
                    self.board.shortestMove(self.AIPlayer, self.humanPlayer, 0)
                    self.board.shortestMove(self.AIPlayer, self.humanPlayer, BOARD_PAWN_DIM - 1)
                except Exception:
                    self.gameEnd = True
                    self.humanPlayerWon = not self.humanTurn
            else:
                if self.humanTurn:
                    self.humanPlayer.playMove(move)
                else:
                    self.AIPlayer.playMove(move)
            
            # Verify if the game has finished and change the values of gameEnd and humanPlayerWon
            AIPlayerWon = self.AIPlayer.isOnOppositeRow()
            humanPlayerWon = self.humanPlayer.isOnOppositeRow()

            if AIPlayerWon or humanPlayerWon:
                self.gameEnd = True
                self.humanPlayerWon = humanPlayerWon

            self.humanTurn = not self.humanTurn
        except Exception as err:
            print(err)

    def getAllActions(self):
        if self.humanTurn:
            return self.board.getAllActionsForAPlayer(self.humanPlayer, self.AIPlayer)
        else:
            return self.board.getAllActionsForAPlayer(self.AIPlayer, self.humanPlayer)

    def gameFinished(self) -> bool:
        return self.gameEnd

    def humanWon(self) -> bool:
        return self.humanPlayerWon

    def simulateGame(self) -> int:
        score1 = self.board.shortestMove(self.AIPlayer, self.humanPlayer, 0)
        score2 = self.board.shortestMove(self.humanPlayer, self.AIPlayer, BOARD_PAWN_DIM - 1)
        if score1 == score2:
            if self.humanTurn:
                score2 -= 1
            else:
                score1 -= 1

        return score1 - score2

    def deepCopy(self) -> 'Game':
        game = Game(self.humanTurn)
        game.humanPlayer = self.humanPlayer.deepCopy()
        game.AIPlayer = self.AIPlayer.deepCopy()
        game.board = self.board.deepCopy(game.AIPlayer, game.humanPlayer)
        
        # these should not be necessary, but for making a complete deep copy of the game
        game.gameEnd = self.gameEnd
        game.humanPlayerWon = self.humanPlayerWon

        return game

    