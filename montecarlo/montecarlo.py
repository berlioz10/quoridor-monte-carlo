import random
from game.game import Game
from montecarlo.node import Node

class MonteCarlo:
    def __init__(self, humanFirstTurn : bool = True):
        game = Game(humanFirstTurn)

        self.root : Node = Node(None, game, None)

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
        if node.gameFinished() or not node.simulatedOnce:
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
        score = node.simulateGame()
        
        # Also add random walls in front of them from each player if they have
        # TODO
        
        if score > 0:
            return True

        return False

    # backpropagation:
    # after simulations, all the nodes that comes from the root until the node simulated, must be updated:
    # we go through all parents until we meet the root and update it with the new values
    def backpropagation(self, node: Node, AIWon: bool) -> None:

        while node is not None:
            node.updateVisits(AIWon)
            node = node.parent


    # running all the monte carlo tree search steps
    def run(self, no: int = 2000):
        for i in range(no):
            #print(i)
            node : Node = self.selection()
            node, _ = self.expansion(node)
            AIWon : bool = self.simulation(node)
            self.backpropagation(node, AIWon)

    def letAImakeNextMove(self):
        if self.root.game.humanTurn == True:
            raise Exception("It is not AI's turn!")
        best_child_winrate = max(self.root.children, key=lambda x : x.win_games / x.total_games)
        winrate = best_child_winrate.win_games / best_child_winrate.total_games
        print("Winrate: " + str(winrate))
        print("No. old root children: " + str(len(self.root.children)))
        
        ucb_max_children = list(filter(lambda x: x.win_games / x.total_games == winrate, self.root.children))

        self.root = random.choice(ucb_max_children)
        print("Move applied: " + str(self.root.move))
        self.root.parent = None

    def letPlayerMakeNextMove(self, move: tuple | str):
        if self.root.game.humanTurn == False:
            raise Exception("It is not human's turn!")
        
        for child in self.root.children:
            if child.move == move:
                print("Old winrate: " + str(self.root.win_games / self.root.total_games))
                self.root = child
                self.root.parent = None
                
                print("New winrate: " + str(self.root.win_games / self.root.total_games))
                print("No. new root children: " + str(len(self.root.children)))
                return
        
        
        raise Exception("Impossible move!")

