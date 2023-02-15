from math import log, sqrt
import random
from game.game import Game
from utils.consts import INFINITE

class Node:
    def __init__(self, parent: 'Node', game: Game, move: tuple | str | None):
        self.children : list[Node] = []
        self.parent : Node = parent

        # select the move
        self.move = move

        self.game = game

        self.total_games = 0
        self.win_games = 0

    def createChildren(self):

        all_actions = self.game.getAllActions()

        for action in all_actions:
            game = self.game.deepCopy()
            game.nextMove(action)
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
        ucb_max_children = list(filter(lambda x: x.UCBScore() == ucb_max_score, self.children))

        return random.choice(ucb_max_children)


    def updateVisits(self, win : bool = False):
        # alternative: rollout
        self.total_games += 1
        if win:
            self.win_games += 1

    def gameFinished(self) -> bool:
        return self.game.gameFinished()

    def humanWon(self) -> bool:
        return self.game.humanWon()