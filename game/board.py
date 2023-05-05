import copy
from game.player import Player
from utils.consts import BOARD_PAWN_DIM, BOARD_WALL_DIM, DOWN, DOWN_DOWN, DOWN_LEFT, DOWN_RIGHT, HORIZONTAL, LEFT, LEFT_LEFT, NO_WALLS, NONE_WALL, RIGHT, RIGHT_RIGHT, UP, UP_LEFT, UP_RIGHT, UP_UP, VERTICAL

class Board:
    def __init__(self, player1: Player, player2: Player, deepcopy = False):
        self.walls_allowed = []
        self.walls_used = []
        self.leftRight = []
        self.upDown = []
        
        if not deepcopy:
            for _ in range(BOARD_WALL_DIM):
                self.walls_allowed.append({HORIZONTAL: [True for _ in range(BOARD_WALL_DIM)], VERTICAL: [True for _ in range(BOARD_WALL_DIM)]})
                self.walls_used.append([NONE_WALL for _ in range(BOARD_WALL_DIM)])

        # left-right
        # for _ in range(BOARD_PAWN_DIM):
        #    self.leftRight.append([True for _ in range(BOARD_WALL_DIM)]) 

        # up-down
        # for _ in range(BOARD_WALL_DIM):
        #    self.leftRight.append([True for _ in range(BOARD_PAWN_DIM)])

        self.player1 = player1
        self.player2  = player2

    def get_all_actions_for_a_player(self, player_move: Player, other_player: Player):
        actions_list = []
        
        # walls allowed ( only if the player has anymore walls to use)
        if player_move.no_walls != 0:
            for i in range(BOARD_WALL_DIM):
                for j in range(BOARD_WALL_DIM):
                    if self.walls_allowed[i][HORIZONTAL][j] == True:
                        if player_move.no_walls == NO_WALLS and other_player.no_walls == NO_WALLS:
                            actions_list.append((i, j, HORIZONTAL))
                        else:
                            self.walls_used[i][j] = HORIZONTAL
                            score1 = self.shortest_path_score(player_move, other_player, player_move.end_line)
                            score2 = self.shortest_path_score(other_player, player_move, other_player.end_line)
                            if not score1 == -1 and not score2 == -1:
                                actions_list.append((i, j, HORIZONTAL))
                            self.walls_used[i][j] = NONE_WALL
                    if self.walls_allowed[i][VERTICAL][j] == True:
                        if player_move.no_walls == NO_WALLS and other_player.no_walls == NO_WALLS:
                            actions_list.append((i, j, VERTICAL))
                        else:
                            self.walls_used[i][j] = VERTICAL
                            score1 = self.shortest_path_score(player_move, other_player, player_move.end_line)
                            score2 = self.shortest_path_score(other_player, player_move, other_player.end_line)
                            if not score1 == -1 and not score2 == -1:
                                actions_list.append((i, j, VERTICAL))
                            self.walls_used[i][j] = NONE_WALL
        
        # the moves the player which moves is allowed ( without considering the other player, only as a "wall")
        actions_list = actions_list + self.get_simple_moves(player_move, other_player)

        actions_list = actions_list + self.get_near_player_moves(player_move, other_player)

        return actions_list

    # tries to put a wall in the board
    # validates if it is out of boundaries, consts are incorrect and etc.
    # if the validation process is ok, then places a wall
    # and sets the allowance of other walls near it
    # x, y - numbers, coordinates of the wall
    # position - VERTICAL or HORIZONTAL ( consts), how the wall should be put
    def use_wall(self, x: int, y: int, position: str):
        if x < 0 or x > BOARD_WALL_DIM - 1 or y < 0 or y > BOARD_WALL_DIM - 1:
            raise Exception("Coordinates of the wall are not between 0 and 7") 
        if position != HORIZONTAL and position != VERTICAL:
            raise Exception("Not a possible position: only HORIZONTAL or VERTICAL")

        if self.walls_allowed[x][position][y] == False:
            raise Exception("Wall is not allowed")

        self.walls_allowed[x][HORIZONTAL][y] = False
        self.walls_allowed[x][VERTICAL][y] = False
        self.walls_used[x][y] = position

        if position == HORIZONTAL:
            if y > 0:
                self.walls_allowed[x][HORIZONTAL][y - 1] = False
                
            
            if y < BOARD_WALL_DIM - 1:
                self.walls_allowed[x][HORIZONTAL][y + 1] = False 
        
        
        if position == VERTICAL:
            if x > 0:
                self.walls_allowed[x - 1][VERTICAL][y] = False
            
            if x < BOARD_WALL_DIM - 1:
                self.walls_allowed[x + 1][VERTICAL][y] = False

    # validates all simple moves and return them as a list
    # this is a simple version, as in it does not interfere with special actions with another player
    # ( like jumping him etc.)
    # playerMove - the player from which we are trying to get the simple moves
    # otherPlayer - the other player ( we need him because he should not make moves that will make 
    # the two pawns have the same coordinates)
    def get_simple_moves(self, player_move: Player, other_player: Player) -> list:
        moves = []

        x = player_move.x
        y = player_move.y

        # verify for UP
        if x != 0 and (x - 1 != other_player.x or y != other_player.y):
            row = self.walls_used[x - 1]
            if y == 0:
                if row[0] != HORIZONTAL:
                    moves.append(UP)
            elif y == BOARD_PAWN_DIM - 1:
                if row[BOARD_WALL_DIM - 1] != HORIZONTAL:
                    moves.append(UP)
            elif row[y] != HORIZONTAL and row[y - 1] != HORIZONTAL:
                moves.append(UP)

        # verify for DOWN
        if x != BOARD_PAWN_DIM - 1 and (x + 1 != other_player.x or y != other_player.y):    
            row = self.walls_used[x]
            if y == 0:
                if row[0] != HORIZONTAL:
                    moves.append(DOWN)
            elif y == BOARD_PAWN_DIM - 1:
                if row[BOARD_WALL_DIM - 1] != HORIZONTAL:
                    moves.append(DOWN)
            elif row[y] != HORIZONTAL and row[y - 1] != HORIZONTAL:
                moves.append(DOWN)

        # validate for LEFT
        if y != 0 and (x != other_player.x or y - 1 != other_player.y):
            column_index = y - 1
            if x == 0:
                if self.walls_used[x][column_index] != VERTICAL:
                    moves.append(LEFT)
            elif x == BOARD_PAWN_DIM - 1:
                if self.walls_used[BOARD_WALL_DIM - 1][column_index] != VERTICAL:
                    moves.append(LEFT)
            elif self.walls_used[x][column_index] != VERTICAL and self.walls_used[x - 1][column_index] != VERTICAL:
                moves.append(LEFT)

        # validate for RIGHT
        if y != BOARD_PAWN_DIM - 1 and (x != other_player.x or y + 1 != other_player.y):
            column_index = y
            if x == 0:
                if self.walls_used[x][column_index] != VERTICAL:
                    moves.append(RIGHT)
            elif x == BOARD_PAWN_DIM - 1:
                if self.walls_used[BOARD_WALL_DIM - 1][column_index] != VERTICAL:
                    moves.append(RIGHT)
            elif self.walls_used[x][column_index] != VERTICAL and self.walls_used[x - 1][column_index] != VERTICAL:
                moves.append(RIGHT)

        return moves

    def get_near_player_moves(self, playerMove: Player, otherPlayer: Player) -> list:
        # see if the players are close to each other
        okNearPlayer = False
        if playerMove.x == otherPlayer.x:
            # left
            if playerMove.y == otherPlayer.y + 1:
                ok1 = True
                ok2 = True
                if playerMove.x > 0:
                    if self.walls_used[playerMove.x - 1][playerMove.y - 1] == VERTICAL:
                        ok1 = False
                if playerMove.x < BOARD_PAWN_DIM - 1:
                    if self.walls_used[playerMove.x][playerMove.y - 1] == VERTICAL:
                        ok2 = False

                if ok1 and ok2:
                    okNearPlayer = True
            # right
            if playerMove.y == otherPlayer.y - 1:
                ok1 = True
                ok2 = True
                if playerMove.x > 0:
                    if self.walls_used[playerMove.x - 1][playerMove.y] == VERTICAL:
                        ok1 = False
                if playerMove.x < BOARD_PAWN_DIM - 1:
                    if self.walls_used[playerMove.x][playerMove.y] == VERTICAL:
                        ok2 = False

                if ok1 and ok2:
                    okNearPlayer = True

        if playerMove.y == otherPlayer.y:
            # up
            if playerMove.x == otherPlayer.x + 1:
                ok1 = True
                ok2 = True
                if playerMove.y > 0:
                    if self.walls_used[playerMove.x - 1][playerMove.y - 1] == HORIZONTAL:
                        ok1 = False
                if playerMove.y < BOARD_PAWN_DIM - 1:
                    if self.walls_used[playerMove.x - 1][playerMove.y] == HORIZONTAL:
                        ok2 = False

                if ok1 and ok2:
                    okNearPlayer = True
            if playerMove.x == otherPlayer.x - 1:
                ok1 = True
                ok2 = True
                if playerMove.y > 0:
                    if self.walls_used[playerMove.x][playerMove.y - 1] == HORIZONTAL:
                        ok1 = False
                if playerMove.y < BOARD_PAWN_DIM - 1:
                    if self.walls_used[playerMove.x][playerMove.y] == HORIZONTAL:
                        ok2 = False

                if ok1 and ok2:
                    okNearPlayer = True

        if okNearPlayer == False:
            return []

        moves = []

        # verify if the player is UP
        if playerMove.x == otherPlayer.x + 1:
            # verify there is no border behind the pawn for UP UP
            if otherPlayer.x != 0:
                okMove = False
                if otherPlayer.y == 0:
                    if self.walls_used[otherPlayer.x - 1][otherPlayer.y] != HORIZONTAL:
                        moves.append(UP_UP)
                        okMove = True
                elif otherPlayer.y == BOARD_PAWN_DIM - 1:
                    if self.walls_used[otherPlayer.x - 1][otherPlayer.y - 1] != HORIZONTAL:
                        moves.append(UP_UP)
                        okMove = True    
                elif self.walls_used[otherPlayer.x - 1][otherPlayer.y - 1] != HORIZONTAL and self.walls_used[otherPlayer.x - 1][otherPlayer.y] != HORIZONTAL:
                    moves.append(UP_UP)
                    okMove = True
                
                if okMove == False:
                    if otherPlayer.y > 0:
                        if self.walls_used[otherPlayer.x][otherPlayer.y - 1] != VERTICAL and self.walls_used[otherPlayer.x - 1][otherPlayer.y - 1] != VERTICAL:
                            moves.append(UP_LEFT)
                    if otherPlayer.y < BOARD_PAWN_DIM - 1:
                        if self.walls_used[otherPlayer.x][otherPlayer.y] != VERTICAL and self.walls_used[otherPlayer.x - 1][otherPlayer.y] != VERTICAL:
                            moves.append(UP_RIGHT)
            # then it means it is on the first row, so it may be possible to jump LEFT UP or RIGHT UP
            else:
                # verify for LEFT UP
                if otherPlayer.y > 0:
                    if self.walls_used[0][otherPlayer.y - 1] != VERTICAL:
                        moves.append(UP_LEFT)
                # verify for RIGHT UP
                if otherPlayer.y < BOARD_PAWN_DIM - 1:
                    if self.walls_used[0][otherPlayer.y] != VERTICAL:
                        moves.append(UP_RIGHT)
           
        # verify if the player is DOWN
        if playerMove.x == otherPlayer.x - 1:
            # verify there is no border behind the pawn for DOWN DOWN
            if otherPlayer.x != BOARD_PAWN_DIM - 1:
                okMove = False
                if otherPlayer.y == 0:
                    if self.walls_used[otherPlayer.x][otherPlayer.y] != HORIZONTAL:
                        moves.append(DOWN_DOWN)
                        okMove = True
                elif otherPlayer.y == BOARD_PAWN_DIM - 1:
                    if self.walls_used[otherPlayer.x][otherPlayer.y - 1] != HORIZONTAL:
                        moves.append(DOWN_DOWN)
                        okMove = True    
                elif self.walls_used[otherPlayer.x][otherPlayer.y - 1] != HORIZONTAL and self.walls_used[otherPlayer.x][otherPlayer.y] != HORIZONTAL:
                    moves.append(DOWN_DOWN)
                    okMove = True
                
                if okMove == False:
                    if otherPlayer.y > 0:
                        if self.walls_used[otherPlayer.x][otherPlayer.y - 1] != VERTICAL and self.walls_used[otherPlayer.x - 1][otherPlayer.y - 1] != VERTICAL:
                            moves.append(DOWN_LEFT)
                    if otherPlayer.y < BOARD_PAWN_DIM - 1:
                        if self.walls_used[otherPlayer.x][otherPlayer.y] != VERTICAL and self.walls_used[otherPlayer.x - 1][otherPlayer.y] != VERTICAL:
                            moves.append(DOWN_RIGHT)
            # then it means it is on the last row, so it may be possible to jump LEFT DOWN or RIGHT DOWN
            else:
                # verify for LEFT DOWN
                if otherPlayer.y > 0:
                    if self.walls_used[otherPlayer.x - 1][otherPlayer.y - 1] != VERTICAL:
                        moves.append(DOWN_LEFT)
                # verify for RIGHT DOWN
                if otherPlayer.y < BOARD_PAWN_DIM - 1:
                    if self.walls_used[otherPlayer.x - 1][otherPlayer.y] != VERTICAL:
                        moves.append(DOWN_RIGHT)

        # verify if the player is LEFT
        if playerMove.y == otherPlayer.y + 1:
            # verify there is no border behind the pawn for LEFT LEFT
            if otherPlayer.y != 0:
                okMove = False
                if otherPlayer.x == 0:
                    if self.walls_used[otherPlayer.x][otherPlayer.y - 1] != VERTICAL:
                        moves.append(LEFT_LEFT)
                        okMove = True
                elif otherPlayer.x == BOARD_PAWN_DIM - 1:
                    if self.walls_used[otherPlayer.x - 1][otherPlayer.y - 1] != VERTICAL:
                        moves.append(LEFT_LEFT)
                        okMove = True    
                elif self.walls_used[otherPlayer.x - 1][otherPlayer.y - 1] != VERTICAL and self.walls_used[otherPlayer.x][otherPlayer.y - 1] != VERTICAL:
                    moves.append(LEFT_LEFT)
                    okMove = True
                
                if okMove == False:
                    if otherPlayer.x > 0:
                        if self.walls_used[otherPlayer.x - 1][otherPlayer.y - 1] != HORIZONTAL and self.walls_used[otherPlayer.x - 1][otherPlayer.y] != HORIZONTAL:
                            moves.append(UP_LEFT)
                    if otherPlayer.x < BOARD_PAWN_DIM - 1:
                        if self.walls_used[otherPlayer.x][otherPlayer.y] != HORIZONTAL and self.walls_used[otherPlayer.x][otherPlayer.y - 1] != HORIZONTAL:
                            moves.append(DOWN_LEFT)
            # then it means it is on the first column, so it may be possible to jump LEFT UP or LEFT DOWN
            else:
                # verify for LEFT UP
                if otherPlayer.x > 0:
                    if self.walls_used[otherPlayer.x - 1][0] != HORIZONTAL:
                        moves.append(UP_LEFT)
                # verify for LEFT DOWN
                if otherPlayer.x < BOARD_PAWN_DIM - 1:
                    if self.walls_used[otherPlayer.x][0] != HORIZONTAL:
                        moves.append(DOWN_LEFT)

        
        # verify if the player is RIGHT
        if playerMove.y == otherPlayer.y - 1:
            # verify there is no border behind the pawn for RIGHT RIGHT
            if otherPlayer.y != BOARD_PAWN_DIM - 1:
                okMove = False
                if otherPlayer.x == 0:
                    if self.walls_used[otherPlayer.x][otherPlayer.y] != VERTICAL:
                        moves.append(RIGHT_RIGHT)
                        okMove = True
                elif otherPlayer.x == BOARD_PAWN_DIM - 1:
                    if self.walls_used[otherPlayer.x - 1][otherPlayer.y] != VERTICAL:
                        moves.append(RIGHT_RIGHT)
                        okMove = True    
                elif self.walls_used[otherPlayer.x - 1][otherPlayer.y] != VERTICAL and self.walls_used[otherPlayer.x][otherPlayer.y] != VERTICAL:
                    moves.append(RIGHT_RIGHT)
                    okMove = True
                
                if okMove == False:
                    if otherPlayer.x > 0:
                        if self.walls_used[otherPlayer.x - 1][otherPlayer.y] != HORIZONTAL and self.walls_used[otherPlayer.x - 1][otherPlayer.y - 1] != HORIZONTAL:
                            moves.append(UP_RIGHT)
                    if otherPlayer.x < BOARD_PAWN_DIM - 1:
                        if self.walls_used[otherPlayer.x][otherPlayer.y - 1] != HORIZONTAL and self.walls_used[otherPlayer.x][otherPlayer.y] != HORIZONTAL:
                            moves.append(DOWN_RIGHT)
            # then it means it is on the last column, so it may be possible to jump RIGHT UP or RIGHT DOWN
            else:
                # verify for RIGHT UP
                if otherPlayer.x > 0:
                    if self.walls_used[otherPlayer.x - 1][otherPlayer.y - 1] != HORIZONTAL:
                        moves.append(UP_RIGHT)
                # verify for RIGHT DOWN
                if otherPlayer.x < BOARD_PAWN_DIM - 1:
                    if self.walls_used[otherPlayer.x][otherPlayer.y - 1] != HORIZONTAL:
                        moves.append(DOWN_RIGHT)

        return moves

    # calculates how many more moves it has to make until it arrives to the opposite row
    # also it has to be mentioned that it finds the path with the shortest number of moves
    # it uses Lee's Algorithm
    def shortest_path_score(self, player: Player, otherPlayer: Player, winningRow: int) -> int:
        # calculate the shortest path to the end

        insignifiantPlayer = Player()
        insignifiantPlayer.x = -2
        insignifiantPlayer.y = -2
        lee = [[0 for _ in range(BOARD_PAWN_DIM)] for _ in range(BOARD_PAWN_DIM)]

        moves = { 
            DOWN: [1, 0], 
            UP: [-1, 0], 
            RIGHT: [0, 1], 
            LEFT: [0, -1],
            DOWN_DOWN: [2, 0],
            DOWN_RIGHT: [1, 1],
            RIGHT_RIGHT: [0, 2],
            UP_RIGHT: [-1, 1],
            UP_UP: [-2, 0],
            UP_LEFT: [-1, -1],
            LEFT_LEFT: [0, -2],
            DOWN_LEFT: [1, -1]
        }

        q = [[player.x, player.y]]

        lee[player.x][player.y] = 1
        while len(q) != 0:
            pos = q.pop(0)
            newPlayerPosition = Player()
            newPlayerPosition.x = pos[0]
            newPlayerPosition.y = pos[1]
            simple_moves = self.get_simple_moves(newPlayerPosition, insignifiantPlayer)
            special_moves = self.get_near_player_moves(newPlayerPosition, otherPlayer)
            # simple moves
            for move in simple_moves:
                x = pos[0] + moves[move][0]
                y = pos[1] + moves[move][1]
                
                if lee[pos[0]][pos[1]] + 1 < lee[x][y] or lee[x][y] == 0:
                    lee[x][y] = lee[pos[0]][pos[1]] + 1  
                    q.append([x, y])
            
            # special moves ( players that are next to each other)
            for move in special_moves:
                x = pos[0] + moves[move][0]
                y = pos[1] + moves[move][1]

                if lee[pos[0]][pos[1]] + 1 < lee[x][y] or lee[x][y] == 0:
                        lee[x][y] = lee[pos[0]][pos[1]] + 1  
                        q.append([x, y])
            
        min_values = [x for x in lee[winningRow] if x != 0]

        if len(min_values) == 0:
            return -1
        '''
        for row in lee:
            for el in row:
                print(el, end=" ")
            print()
        '''        
        ct = min(min_values)

        return ct - 1

    def shortest_path_move(self, player: Player, other_player: Player, winning_row: int) -> str:
        # calculate the shortest path to the end
        lee = [[[0, ""] for _ in range(BOARD_PAWN_DIM)] for _ in range(BOARD_PAWN_DIM)]

        moves = { 
            DOWN: [1, 0], 
            UP: [-1, 0], 
            RIGHT: [0, 1], 
            LEFT: [0, -1],
            DOWN_DOWN: [2, 0],
            DOWN_RIGHT: [1, 1],
            RIGHT_RIGHT: [0, 2],
            UP_RIGHT: [-1, 1],
            UP_UP: [-2, 0],
            UP_LEFT: [-1, -1],
            LEFT_LEFT: [0, -2],
            DOWN_LEFT: [1, -1]
        }

        q = [[player.x, player.y]]

        lee[player.x][player.y][0] = 1
        while len(q) != 0:
            pos = q.pop(0)
            new_player_position = Player()
            new_player_position.x = pos[0]
            new_player_position.y = pos[1]
            simple_moves = self.get_simple_moves(new_player_position, other_player)
            special_moves = self.get_near_player_moves(new_player_position, other_player)
            # simple moves
            for move in simple_moves + special_moves:
                x = pos[0] + moves[move][0]
                y = pos[1] + moves[move][1]
                
                if lee[pos[0]][pos[1]][0] + 1 < lee[x][y][0] or lee[x][y][0] == 0:
                    if lee[pos[0]][pos[1]][0] == 1:
                        lee[pos[0]][pos[1]][1] = move
                    lee[x][y][0] = lee[pos[0]][pos[1]][0] + 1
                    lee[x][y][1] = lee[pos[0]][pos[1]][1]
                    q.append([x, y])
            
        min_values = [x for x in lee[winning_row] if x[0] != 0]

        if len(min_values) == 0:
            return ""
        
        '''
        for row in lee:
            for el in row:
                print(el, end=" ")
            print()
        '''        
        ct = min(min_values)

        return ct[1]

    def deepcopy(self, player1: Player, player2: Player) -> 'Board':
        board = Board(player1, player2, deepcopy=True)

        board.walls_allowed = []
        board.walls_used = []

        for i in range(BOARD_WALL_DIM):
            board.walls_allowed.append({HORIZONTAL: [self.walls_allowed[i][HORIZONTAL][j] for j in range(BOARD_WALL_DIM)], VERTICAL: [self.walls_allowed[i][VERTICAL][j] for j in range(BOARD_WALL_DIM)]})
            board.walls_used.append([self.walls_used[i][j] for j in range(BOARD_WALL_DIM)])

        return board
    
    def reset(self):
        for i in range(BOARD_WALL_DIM):
            for j in range(BOARD_WALL_DIM):
                self.walls_allowed[i][HORIZONTAL][j] = True
                self.walls_allowed[i][VERTICAL][j] = True
                self.walls_used[i][j] = NONE_WALL