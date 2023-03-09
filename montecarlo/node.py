import copy
from math import log, sqrt
import random
from game.game import Game
from utils.consts import INFINITE

class Node:
    def __init__(self, parent: 'Node | None', game: Game, move: tuple | str | None):
        self.children : list[Node] = []
        self.parent : Node | None = parent

        # select the move
        self.move = move

        self.game = game
        self.simulatedOnce = False
        self.total_games = 0
        self.win_games = 0

    def createChildren(self):

        all_actions = self.game.getAllActions()
        
        if len(all_actions) == 0:
            node = self
            while node is not None:
                node = node.parent

        for action in all_actions:
            game = self.game.deepCopy()
            game.makeMove(action)
            node = Node(self, game, action)
            self.children.append(node)

    def UCBScore(self) -> float:

        # for the root, we cannot calculate the UCB score
        if self.parent == None:
            raise Exception("Cannot calculate for a node without a parent")

        # as other papers mentioned, we favour exploration, not exploitation
        if self.total_games == 0:
            return INFINITE

        # C is the bias, usually square root of 2
        c = sqrt(2)

        # formula for UCB Score
        
        return self.win_games / self.total_games + c * sqrt(log(self.parent.total_games) / self.total_games)

    def selectRandomChildWithBestUCBScore(self) -> 'Node':

        ucb_max_score = max(self.children, key=lambda x : x.UCBScore())
        # print("Winrate: " + str(ucb_max_score))
        # print("No. children: " + str(len(self.children)))
        
        ucb_max_children = list(filter(lambda x: x.UCBScore() == ucb_max_score.UCBScore(), self.children))

        return random.choice(ucb_max_children)

    def simulateGame(self) -> int:
        self.simulatedOnce = True
        return self.game.simulateGameV2()

    def updateVisits(self, win : bool = False):
        # alternative: rollout
        self.total_games += 1
        if win:
            self.win_games += 1

    def gameFinished(self) -> bool:
        return self.game.gameFinished()

    def humanWon(self) -> bool:
        return self.game.humanWon()