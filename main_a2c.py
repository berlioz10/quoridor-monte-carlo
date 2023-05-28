import torch
from game.game import Game
from montecarlo.montecarlo import MonteCarlo
from network.actor_critic_conv import ActorCriticConv
from utils.consts import BOARD_PAWN_DIM, DOWN, HORIZONTAL, INFINITE, LEFT, RIGHT, SAVED_NETWORKS_DIR, UP, VERTICAL

# test cases for: 
# board (simulatePlayer, walls allowed, player position)
# 
# TODO
if __name__ == '__main__':
    ok_human_turn = True

    model = ActorCriticConv()

    model.load_state_dict(torch.load(SAVED_NETWORKS_DIR + "test.pt"))
    
    game = Game(human_turn=ok_human_turn)
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
        if game.game_finished():
            print("The winner is ", end="")
            if game.human_won():
                print("the person!")
            else:
                print("the A2C!")
        
            break
        
        if ok_human_turn:
            x = input("Write your move: ")
            ok = True
            while ok:
                possible_tuple = x.split() 
                if len(possible_tuple) > 1:
                    x = (int(possible_tuple[0]), int(possible_tuple[1]), possible_tuple[2])
                
                try: 
                    game.make_move(x)
                    ok = False
                except Exception:
                    x = input("Move doesn't exist or it is impossible, try again: ")
        else:
            policy, value = model(game.get_convolutional_layer())    
            ok = True
            while ok:
                action = torch.argmax(policy)
                move = Game.convert_action_into_move(action)
                print(move)
                reward, done = game.step(action)
                if reward == -30:
                    policy[action] = -1.0 * INFINITE
                else:
                    ok = False

        game.print_game()

        ok_human_turn = not ok_human_turn
