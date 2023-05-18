import random
import numpy as np
from game.board import Board
from game.player import Player
from utils.consts import BOARD_PAWN_DIM, BOARD_WALL_DIM, DOWN, DOWN_DOWN, DOWN_LEFT, DOWN_RIGHT, HORIZONTAL, LEFT, LEFT_LEFT, NO_WALLS, NONE_WALL, RIGHT, RIGHT_RIGHT, UP, UP_LEFT, UP_RIGHT, UP_UP, VERTICAL

class Game:
    # a board
    # players - 2
    # human first turn or not
    def __init__(self, human_turn : bool = True, deep_copy = False):

        if not deep_copy:        
            self.human_player : Player = Player(human=True)
            self.AI_player : Player = Player(human=False)

            self.board : Board = Board(player1=self.human_player, player2=self.AI_player)
        
        self.human_turn = human_turn
        self.game_end = False
        self.human_player_won = None

    # TODO: add comment
    def make_move(self, move: tuple | str):
        try:
            # wall is used
            if type(move) is tuple:
                # adding a new rule for AI:
                if self.human_turn:
                    self.human_player.decrement_walls()
                else:
                    self.AI_player.decrement_walls()
                self.board.use_wall(move[0], move[1], move[2])
                score1 = 0
                score2 = 0
                score1 = self.board.shortest_path_score(self.AI_player, self.human_player, 0)
                score2 = self.board.shortest_path_score(self.human_player, self.AI_player, BOARD_PAWN_DIM - 1)
                if score1 == -1 or score2 == -1:
                    self.game_end = True
                    self.human_player_won = not self.human_turn
            else:
                if self.human_turn:
                    self.human_player.play_move(move)
                else:
                    self.AI_player.play_move(move)
            
            # Verify if the game has finished and change the values of gameEnd and human_player_won
            AI_player_won = self.AI_player.is_on_opposite_row()
            human_player_won = self.human_player.is_on_opposite_row()

            if AI_player_won or human_player_won:
                self.game_end = True
                self.human_player_won = human_player_won

            self.human_turn = not self.human_turn
        except Exception as err:
            print(err)

    def get_all_actions(self):
        if self.human_turn:
            return self.board.get_all_actions_for_a_player(self.human_player, self.AI_player)
        else:
            return self.board.get_all_actions_for_a_player(self.AI_player, self.human_player)

    def game_finished(self) -> bool:
        return self.game_end

    def human_won(self) -> bool:
        return self.human_player_won

    def simulate_game(self) -> int:
        try:
            score1 = self.board.shortest_path_score(self.AI_player, self.human_player, 0)
            score2 = self.board.shortest_path_score(self.human_player, self.AI_player, BOARD_PAWN_DIM - 1)
        except Exception:
            self.game_end = True
            self.human_player_won = self.human_turn
            if self.human_turn:
                return -1
            else:
                return 1
        # print(str(score1) + " " + str(score2))
        if score1 == score2:
            if self.human_turn:
                score2 -= 1
            else:
                score1 -= 1
        return score2 - score1

    def simulate_gameV2(self, probability=0.70) -> int:
        game = self.deepcopy()
        #print("Original game!")
        #print(self.board.wallsUsed)
        
        #print("Copy of the game!")
        #print(game.board.wallsUsed)

        while not game.game_finished():
            random_move = random.uniform(0, 1)
            player1 = game.human_player
            player2 = game.AI_player
            dest = BOARD_PAWN_DIM - 1
            if not game.human_turn:
                player1, player2 = player2, player1
                dest = 0

            move = ""

            if player1.no_walls == 0:
                probability = 0.99
            if random_move < probability:
                
                move = game.board.shortest_path_move(player1, player2, dest)
                if move == "":
                    random_move = 1.0
                else:
                    game.make_move(move)

            if random_move >= probability:
                moves = game.board.get_all_actions_for_a_player(player1, player2)
                move = random.choice(moves)
                # print("Random move: " + str(move))
                game.make_move(move)
            # game.printGame()
        
        if game.human_won():
            return -1
        return 1

    def deepcopy(self) -> 'Game':
        game = Game(True if self.human_turn else False, deep_copy=True)
        game.human_player = self.human_player.deepcopy()
        game.AI_player = self.AI_player.deepcopy()
        game.board = self.board.deepcopy(game.AI_player, game.human_player)
        
        # these should not be necessary, but for making a complete deep copy of the game
        game.game_end = self.game_end
        game.human_player_won = self.human_player_won

        return game
    
    def print_game(self):
        print_matrix = [[' ' for _ in range(BOARD_PAWN_DIM * 2 - 1)] for _ in range(BOARD_PAWN_DIM * 2 - 1)]
        for i in range(BOARD_WALL_DIM):
            for j in range(BOARD_WALL_DIM):
                if self.board.walls_used[i][j] == HORIZONTAL:
                    print_matrix[i * 2 + 1][j * 2 + 1] = '#'
                    print_matrix[i * 2 + 1][j * 2 + 0] = '#'
                    print_matrix[i * 2 + 1][j * 2 + 2] = '#'
                elif self.board.walls_used[i][j] == VERTICAL:
                    print_matrix[i * 2 + 1][j * 2 + 1] = '#'
                    print_matrix[i * 2 + 0][j * 2 + 1] = '#'
                    print_matrix[i * 2 + 2][j * 2 + 1] = '#'

        for i in range(BOARD_PAWN_DIM):
            for j in range(BOARD_PAWN_DIM):
                print_matrix[i * 2][j * 2] = '-'
        
        print_matrix[self.human_player.x * 2][self.human_player.y * 2] = 'O'
        print_matrix[self.AI_player.x * 2][self.AI_player.y * 2] = 'X'

        for row in print_matrix:
            for el in row:
                print(el, end=" ")
            print()
        print("\n")

    def get_linear_state(self) -> np.array:
        # make a linear array from the walls position
        walls = np.array(self.board.walls_used).reshape((BOARD_WALL_DIM * BOARD_WALL_DIM))
        walls[walls == NONE_WALL] = 0
        walls[walls == HORIZONTAL] = 1
        walls[walls == VERTICAL] = 2
        
        pawns = np.zeros((BOARD_PAWN_DIM * BOARD_PAWN_DIM))
        pawns[self.human_player.x * BOARD_PAWN_DIM + self.human_player.y] = 1
        pawns[self.AI_player.x * BOARD_PAWN_DIM + self.AI_player.y] = 2

        return np.concatenate((walls, pawns)).astype(float)
    
    def step(self, action: int) -> tuple[int, bool]:
        reward = 0
        done = False

        if action >= 0  and action <= 11:
            if action == 0:
                move = UP
            if action == 1:
                move = DOWN
            if action == 2:
                move = LEFT
            if action == 3:
                move = RIGHT
            if action == 4:
                move = UP_UP
            if action == 5:
                move = DOWN_DOWN
            if action == 6:
                move = LEFT_LEFT
            if action == 7:
                move = RIGHT_RIGHT
            if action == 8:
                move = UP_LEFT
            if action == 9:
                move = UP_RIGHT
            if action == 10:
                move = DOWN_LEFT
            if action == 11:
                move = DOWN_RIGHT
        else:
            action = action - 12
            x = action  // 2 // BOARD_WALL_DIM
            y = action // 2   % BOARD_WALL_DIM
            position = HORIZONTAL if action % 2 == 0 else VERTICAL
            move = (x, y, position)

        actions = self.get_all_actions()
    
        if move not in actions:
            reward = -30
            done = True
        else:
            reward = 0
            self.make_move(move)
            done = self.game_finished()

            game = self.deepcopy()
        
            while not game.game_finished():
                player1 = game.human_player
                player2 = game.AI_player
                if not game.human_turn:
                    player1, player2 = player2, player1
                    
                move = game.board.shortest_path_move(player1, player2, player1.end_line)
                if move == "":
                    moves = game.board.get_all_actions_for_a_player(player1, player2)
                    move = random.choice(moves)
                
                game.make_move(move)
            
            if game.human_won():
                reward -= game.board.shortest_path_score(game.AI_player, game.human_player, game.AI_player.end_line)
            else:
                reward += 3 + game.board.shortest_path_score(game.human_player, game.AI_player, game.human_player.end_line)
        
        # print(move)
        # self.print_game()
        # print(done)
        return reward, done
    
    def make_random_move(self) -> tuple[int, bool]:

        player1 = self.human_player
        player2 = self.AI_player
        if not self.human_turn:
            raise Exception("It should not happen!!!\n")
        move = self.board.shortest_path_move(player1, player2, player1.end_line)
        if move == "":
            moves = self.board.get_all_actions_for_a_player(player1, player2)
            move = random.choice(moves)
        self.make_move(move)

        done = self.game_finished()

        game = self.deepcopy()
        
        while not game.game_finished():
            player1 = game.human_player
            player2 = game.AI_player
            if not game.human_turn:
                player1, player2 = player2, player1
                    
            move = game.board.shortest_path_move(player1, player2, player1.end_line)
            if move == "":
                moves = game.board.get_all_actions_for_a_player(player1, player2)
                move = random.choice(moves)
                
            game.make_move(move)
        
        if game.human_won():
            reward = -5
        else:
            reward = +5

        return reward, done
    
    def reset(self, human_turn=False):
        self.human_player.reset()
        self.AI_player.reset()
        self.board.reset()
        
        self.human_turn = human_turn
        self.game_end = False
        self.human_player_won = None

    def reset_custom(self, human_turn=False, random_position=False, custom_walls=NO_WALLS):
        self.human_player.reset()
        self.AI_player.reset()
        self.board.reset()
        
        self.human_turn = human_turn
        self.game_end = False
        self.human_player_won = None

        if random_position:
            self.human_player.x = random.randint(0, BOARD_PAWN_DIM // 2 - 1)
            self.human_player.y = random.randint(0, BOARD_PAWN_DIM)

            self.AI_player.x = random.randint(BOARD_PAWN_DIM // 2 + 1, BOARD_PAWN_DIM - 1)
            self.AI_player.y = random.randint(0, BOARD_PAWN_DIM)

        self.human_player.no_walls = custom_walls
        self.AI_player.no_walls = custom_walls

        for _ in range((NO_WALLS - custom_walls) * 2):
            x = random.randint(0, BOARD_WALL_DIM)
            y = random.randint(0, BOARD_WALL_DIM)

            position = VERTICAL if random.randint(0, 1) else HORIZONTAL

            while self.board.use_wall_restrictive(x, y, position):
                x = random.randint(0, BOARD_WALL_DIM)
                y = random.randint(0, BOARD_WALL_DIM)

                position = VERTICAL if random.randint(0, 1) != 0 else HORIZONTAL
