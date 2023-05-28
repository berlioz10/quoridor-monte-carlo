import random
from game.game import Game
from montecarlo.node import Node

class MonteCarlo:
    def __init__(self, human_turn : bool = True):
        game = Game(human_turn)

        self.root : Node = Node(None, game, None)

    # selection:
    # choose a leaf, by the best score
    # and return it
    def selection(self) -> Node:
        node : Node = self.root
        # we want to select a node that is a leaf
        while not node.game_finished() and len(node.children) != 0:
            # select by the best UCB
            node = node.select_random_child_with_best_UCB_score()

        return node

    # expansion:
    # after we choose a leaf from selection, we will extend it
    # but if in that node, the game is finished, then we return false
    # ( the return will tell if we simulate the game or not) 
    def expansion(self, node : Node) -> tuple[Node, bool]:
        if node.game_finished() or not node.simulatedOnce:
            return node, False
        node.create_children()

        node = node.select_random_child_with_best_UCB_score()

        return node, True

    # simulation
    # for first, we will simulate only one game of Quoridor, in an heuristic way
    # simulation returns if the AI Player won or not 
    def simulation(self, node: Node) -> bool:
        if node.game_finished():
            return not node.human_won()
        score = node.simulate_game()
        
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
            node.update_visits(AIWon)
            node = node.parent


    # running all the monte carlo tree search steps
    def run(self, no: int = 2000):
        for i in range(no):
            #print(i)
            node : Node = self.selection()
            node, _ = self.expansion(node)
            AI_won : bool = self.simulation(node)
            self.backpropagation(node, AI_won)

    def make_next_move(self):
        if self.root.game.human_turn == True:
            raise Exception("It is not AI's turn!")
        best_child_winrate = max(self.root.children, key=lambda x : x.win_games / x.total_games)
        winrate = best_child_winrate.win_games / best_child_winrate.total_games
        # print("Winrate: " + str(winrate))
        # print("No. old root children: " + str(len(self.root.children)))
        
        ucb_max_children = list(filter(lambda x: x.win_games / x.total_games == winrate, self.root.children))

        self.root = random.choice(ucb_max_children)
        # print("Move applied: " + str(self.root.move))
        self.root.parent = None
        
        print("Monte Carlo's move: " + str(self.root.move))
        return self.root.game.game_end

    def let_player_make_next_move(self, move: tuple | str):
        if self.root.game.human_turn == False:
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
    
    
    def let_player_make_next_action(self, action: int) -> tuple[int, bool]:
        if self.root.game.human_turn == False:
            raise Exception("It is not human's turn!")
        

        reward, done = self.root.game.step(action)

        if reward != -30:
            reward = reward * -1 + 10
            move = Game.convert_action_into_move(action)
            for child in self.root.children:
                if child.move == move:
                    # print("Old winrate: " + str(self.root.win_games / self.root.total_games))
                    self.root = child
                    self.root.parent = None
                    
                    # print("New winrate: " + str(self.root.win_games / self.root.total_games))
                    # print("No. new root children: " + str(len(self.root.children)))
                    break
        

        return reward, done