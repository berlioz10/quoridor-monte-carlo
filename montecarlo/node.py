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

    def create_children(self):

        all_actions = self.game.get_all_actions()
        
        if len(all_actions) == 0:
            node = self
            while node is not None:
                node = node.parent

        for action in all_actions:
            game = self.game.deepcopy()
            game.make_move(action)
            node = Node(self, game, action)
            self.children.append(node)

    def UCB_score(self) -> float:

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

    def select_random_child_with_best_UCB_score(self) -> 'Node':

        ucb_max_score = max(self.children, key=lambda x : x.UCB_score())
        # print("Winrate: " + str(ucb_max_score))
        # print("No. children: " + str(len(self.children)))
        
        ucb_max_children = list(filter(lambda x: x.UCB_score() == ucb_max_score.UCB_score(), self.children))

        return random.choice(ucb_max_children)

    def simulate_game(self) -> int:
        self.simulatedOnce = True
        return self.game.simulate_gameV2()

    def update_visits(self, win : bool = False):
        # alternative: rollout
        self.total_games += 1
        if win:
            self.win_games += 1

    def game_finished(self) -> bool:
        return self.game.game_finished()

    def human_won(self) -> bool:
        return self.game.human_won()