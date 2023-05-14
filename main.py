from game.game import Game
from montecarlo.montecarlo import MonteCarlo
from utils.consts import BOARD_PAWN_DIM, DOWN, HORIZONTAL, LEFT, RIGHT, UP, VERTICAL

# test cases for: 
# board (simulatePlayer, walls allowed, player position)
# 
# TODO
if __name__ == '__main__':
    okHumanTurn = False
    monteCarlo = MonteCarlo(humanFirstTurn=okHumanTurn)
    
    game = Game(human_turn=True)
    '''
    game.makeMove((1, 0, VERTICAL))
    game.makeMove((2, 1, HORIZONTAL))
    game.makeMove((2, 2, VERTICAL))
    game.makeMove((2, 3, HORIZONTAL))
    game.makeMove((3, 0, HORIZONTAL))
    game.makeMove((3, 1, VERTICAL))
    game.makeMove((3, 3, HORIZONTAL))
    game.humanPlayer.x = 1
    game.humanPlayer.y = 2
    game.AIPlayer.x = 2
    game.AIPlayer.y = 2
    '''
    while True:
        if monteCarlo.root.game_finished():
            print("The winner is ", end="")
            if monteCarlo.root.human_won():
                print("the person!")
            else:
                print("the AI!")
        
            break
        
        if okHumanTurn:
            monteCarlo.run(no=130)
            ok = True
            
            x = input("Write your move: ")
            while ok:
                possible_tuple = x.split() 
                if len(possible_tuple) > 1:
                    x = (int(possible_tuple[0]), int(possible_tuple[1]), possible_tuple[2])
                
                try: 
                    monteCarlo.let_player_make_next_move(x)
                    ok = False
                except Exception:
                    x = input("Move doesn't exist or it is impossible, try again: ")
        else:
            monteCarlo.run(no=2000)
            monteCarlo.let_AI_make_next_move()

        monteCarlo.root.game.print_game()

        okHumanTurn = not okHumanTurn