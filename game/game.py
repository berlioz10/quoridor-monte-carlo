import random
from game.board import Board
from game.player import Player
from utils.consts import BOARD_PAWN_DIM, BOARD_WALL_DIM, HORIZONTAL, VERTICAL

class Game:
    # a board
    # players - 2
    # human first turn or not
    def __init__(self, humanFirstTurn : bool = True, deepCopy = False):

        if not deepCopy:        
            self.humanPlayer : Player = Player(human=True)
            self.AIPlayer : Player = Player(human=False)

            self.board : Board = Board(player1=self.humanPlayer, player2=self.AIPlayer)
        
        self.humanTurn = humanFirstTurn
        self.gameEnd = False
        self.humanPlayerWon = None

    # TODO: add comment
    def makeMove(self, move: tuple | str):
        try:
            # wall is used
            if type(move) is tuple:
                # adding a new rule for AI:
                if self.humanTurn:
                    self.humanPlayer.decrementWalls()
                else:
                    self.AIPlayer.decrementWalls()
                self.board.useWall(move[0], move[1], move[2])
                score1 = 0
                score2 = 0
                score1 = self.board.shortestPathScore(self.AIPlayer, self.humanPlayer, 0)
                score2 = self.board.shortestPathScore(self.humanPlayer, self.AIPlayer, BOARD_PAWN_DIM - 1)
                if score1 == -1 or score2 == -1:
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
        try:
            score1 = self.board.shortestPathScore(self.AIPlayer, self.humanPlayer, 0)
            score2 = self.board.shortestPathScore(self.humanPlayer, self.AIPlayer, BOARD_PAWN_DIM - 1)
        except Exception:
            self.gameEnd = True
            self.humanPlayerWon = self.humanTurn
            if self.humanTurn:
                return -1
            else:
                return 1
        # print(str(score1) + " " + str(score2))
        if score1 == score2:
            if self.humanTurn:
                score2 -= 1
            else:
                score1 -= 1
        return score2 - score1

    def simulateGameV2(self) -> int:
        probability = 0.70
        game = self.deepCopy()
        #print("Original game!")
        #print(self.board.wallsUsed)
        
        #print("Copy of the game!")
        #print(game.board.wallsUsed)

        while not game.gameFinished():
            random_move = random.uniform(0, 1)
            player1 = game.humanPlayer
            player2 = game.AIPlayer
            dest = BOARD_PAWN_DIM - 1
            if not game.humanTurn:
                player1, player2 = player2, player1
                dest = 0

            move = ""

            if player1.no_walls == 0:
                probability = 0.99
            if random_move < probability:
                
                move = game.board.shortestPathMove(player1, player2, dest)
                if move == "":
                    random_move = 1.0
                else:
                    game.makeMove(move)

            if random_move >= probability:
                moves = game.board.getAllActionsForAPlayer(player1, player2)
                move = random.choice(moves)
                # print("Random move: " + str(move))
                game.makeMove(move)
            # game.printGame()
        
        if game.humanWon():
            return -1
        return 1

    def deepCopy(self) -> 'Game':
        game = Game(True if self.humanTurn else False, deepCopy=True)
        game.humanPlayer = self.humanPlayer.deepCopy()
        game.AIPlayer = self.AIPlayer.deepCopy()
        game.board = self.board.deepCopy(game.AIPlayer, game.humanPlayer)
        
        # these should not be necessary, but for making a complete deep copy of the game
        game.gameEnd = self.gameEnd
        game.humanPlayerWon = self.humanPlayerWon

        return game
    
    def printGame(self):
        print_matrix = [[' ' for _ in range(BOARD_PAWN_DIM * 2 - 1)] for _ in range(BOARD_PAWN_DIM * 2 - 1)]
        for i in range(BOARD_WALL_DIM):
            for j in range(BOARD_WALL_DIM):
                if self.board.wallsUsed[i][j] == HORIZONTAL:
                    print_matrix[i * 2 + 1][j * 2 + 1] = '#'
                    print_matrix[i * 2 + 1][j * 2 + 0] = '#'
                    print_matrix[i * 2 + 1][j * 2 + 2] = '#'
                elif self.board.wallsUsed[i][j] == VERTICAL:
                    print_matrix[i * 2 + 1][j * 2 + 1] = '#'
                    print_matrix[i * 2 + 0][j * 2 + 1] = '#'
                    print_matrix[i * 2 + 2][j * 2 + 1] = '#'

        for i in range(BOARD_PAWN_DIM):
            for j in range(BOARD_PAWN_DIM):
                print_matrix[i * 2][j * 2] = '-'
        
        print_matrix[self.humanPlayer.x * 2][self.humanPlayer.y * 2] = 'O'
        print_matrix[self.AIPlayer.x * 2][self.AIPlayer.y * 2] = 'X'

        for row in print_matrix:
            for el in row:
                print(el, end=" ")
            print()
        print("\n")

    