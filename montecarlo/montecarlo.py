from game.game import Game
from montecarlo.node import Node

class MonteCarlo:
    def __init__(self, humanFirstTurn : bool = True):
        game = Game(humanFirstTurn)

        self.root : Node = Node(parent=None, game=game, move=None)

    # selection:
    # choose a leaf, by the best score
    # and return it
    def selection(self) -> Node:
        node : Node = self.root
        # we want to select a node that is a leaf
        while not node.gameFinished() and len(node.children) != 0:
            # select by the best UCB
            node = node.selectRandomChildWithBestUCBScore()

        return node

    # expansion:
    # after we choose a leaf from selection, we will extend it
    # but if in that node, the game is finished, then we return false
    # ( the return will tell if we simulate the game or not) 
    def expansion(self, node : Node) -> tuple[Node, bool]:
        if node.gameFinished():
            return node, False

        node.createChildren()

        node = node.selectRandomChildWithBestUCBScore()

        return node, True

    # simulation
    # for first, we will simulate only one game of Quoridor, in an heuristic way
    # simulation returns if the AI Player won or not 
    def simulation(self, node: Node) -> bool:
        if node.gameFinished():
            return not node.humanWon()

        score = node.game.simulateGame()
        # Also add random walls in front of them from each player if they have
        # TODO
        
        if score > 0:
            return True

        return False

    # backpropagation:
    # after simulations, all the nodes that comes from the root until the node simulated, must be updated:
    # we go through all parents until we meet the root and update it with the new values
    def backpropagation(self, node: Node, AIWon: bool) -> None:

        while node.parent != None:
            node.updateVisits(AIWon)
            node = node.parent


    # running all the monte carlo tree search steps
    def run(self, no: int = 2000):
        for _ in range(no):
            node : Node = self.selection()
            node, _ = self.expansion(node)
            AIWon : bool = self.simulation(node)
            self.backpropagation(node, AIWon)
