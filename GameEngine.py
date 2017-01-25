import math
import random
import inspect
import numpy
from copy import deepcopy
from libc.stdlib cimport malloc, free
import c_bindings.get_moves as c_moves


class Piece:
    # 0: Flag
    # 1-7: normal 1 movers, piece 1 loses to spy
    # 8: normal mover, kills bombs
    # 9: super mover
    # 10: bombs, no movement, only loses to miner
    # 11: Spy

    def __init__(self, p, v, a = None):
        self.player = p
        self.value = v
        self.abbrev = a
        self.visible = False
        self.movement = self.get_movement(v)

    def __str__(self):
        return str(self.value)
    __repr__ = __str__

    # returns how many spaces the piece may move.
    def get_movement(self, val):
        if val > 0 and val < 9 or val == 11:
            return 1

        elif val == 9:
            return 100

        else:
            return 0


    def get_visible(self):
        return self.visible


    def get_value(self):
        return self.value


    def get_abbrev(self):
        return self.abbrev


    def get_player(self):
        return self.player


    def reveal(self):
        self.visible = True



class GameEngine:
    def __init__(self, n):
        self.size = n
        self.board = numpy.zeros(0, n * n)
        self.owner = numpy.zeros(0, n * n)
        self.visibility = numpy.zeros(0, n * n)
        self.flags = [[-1, -1], [-1, -1]]
        self.move_history = []


    def convert_to_numpy_1D(b, b2):
        for x in range(self.size):
            for y in range(self.size):
                b2[x + (x * y)] = b[x][y]


    def get_2D_array(b):
        board_temp = [[0 for x in range(0, self.size)] for x in range(0, self.size)]
        for x in range(self.size):
            for y in range(self.size):
                board_temp[x][y] = b[x + (x * y)]
        return board_temp


    def board_setup(self):
        owner_temp = [[0 for x in range(0, self.size)] for x in range(0, self.size)]
        visibility_temp = [[0 for x in range(0, self.size)] for x in range(0, self.size)]
        board_temp = [[0 for x in range(0, self.size)] for x in range(0, self.size)]

        # Rivers
        if self.size == 10:
            board_temp[2][4] = Piece(None, -1, 'K')
            board_temp[2][5] = Piece(None, -1, 'K')
            board_temp[3][4] = Piece(None, -1, 'K')
            board_temp[3][5] = Piece(None, -1, 'K')

            board_temp[6][4] = Piece(None, -1, 'K')
            board_temp[6][5] = Piece(None, -1, 'K')
            board_temp[7][4] = Piece(None, -1, 'K')
            board_temp[7][5] = Piece(None, -1, 'K')
        elif self.size == 6:
            board_temp[2][2] = Piece(None, -1, 'K')
            board_temp[2][3] = Piece(None, -1, 'K')

        for i in range(0, 2):
            if self.size == 10:
                rows = 4
                starting_pieces = [[12, 'Flag F', 1], [10, 'Bomb B', 6], [11, 'Spy Y', 1], [9, 'Scout S', 8], [8, 'Miner R', 5], [7, 'Sergeant T', 4], [6, 'Lieutenent L', 4], [5, 'Captain C', 4], [4, 'Major J', 3], [3, 'Colonel O', 2], [2, 'General G', 1], [1, 'Marshall M', 1]]
            elif self.size == 6:
                rows = 2
                starting_pieces = [[12, 'Flag F', 1], [10, 'Bomb B', 1], [11, 'Spy Y', 1], [9, 'Scout S', 1], [8, 'Miner R', 1], [7, 'Sergeant T', 1], [6, 'Lieutenent L', 1], [5, 'Captain C', 1], [4, 'Major J', 1], [3, 'Colonel O', 1], [2, 'General G', 1], [1, 'Marshall M', 1]]


            starting_locations = []
            randy = random.randrange(0, self.size-1)
            randy2 = random.randrange(0, self.size-1)

            for x in range(0, self.size):
                for y in range(0 + i*(self.size-rows), rows + i*(self.size-rows)):
                    if y == 0 and x == randy and i == 0:
                        owner_temp[x][y] = 0
                        board_temp[x][y] = 12
                        self.flags[0] = [x, y]
                        starting_pieces.pop(0)
                        continue
                    if y == rows + i*(self.size-rows)-1 and x == randy2 and i == 1:
                        owner_temp[x][y] = 1
                        board_temp[x][y] = 12
                        self.flags[1] = [x, y]
                        starting_pieces.pop(0)
                        continue
                    starting_locations.append((x, y, i))

            while len(starting_pieces) != 0:
                r1 = int(random.random()*(len(starting_pieces)))
                r2 = int(random.random()*(len(starting_locations)))

                owner_temp[starting_locations[r2][0]][starting_locations[r2][1]] = starting_locations[r2][2]
                board_temp[starting_locations[r2][0]][starting_locations[r2][1]] = starting_pieces[r1][0]

                starting_locations.pop(r2)
                starting_pieces[r1][2] -= 1
                if starting_pieces[r1][2] == 0:
                    starting_pieces.pop(r1)
        convert_to_numpy_1D(board_temp, self.visibility)
        convert_to_numpy_1D(owner_temp, self.visibility)
        convert_to_numpy_1D(visibility_temp, self.visibility)

    def print_board(self):
        board_to_print = self.get_2D_array(self.board)
        # owner_board = self.get_2D_array(self.owner)
        print()
        for x in range(self.size):
            arr_temp = []
            for y in range(self.size):
                if board_to_print[y][x]:
                    val = board_to_print[y][x].get_value()
                    if val == 0:
                        name = 'F'
                    elif val == 10:
                        name = 'B'
                    elif val == 11:
                        name = 'S'
                    elif val == -1:
                        name = 'L'
                    else:
                        name = val
                    arr_temp.append(name)
                else:
                    arr_temp.append(0)
            print(' '.join(map(str, arr_temp)))
        print()




    # Takes in coord1 [x1, y1] and coord2 [x2, y2], and player = (0 or 1)
    # Assumes there is a piece ar coord1
    # def check_legal(self, coord1, coord2, player):
    #     piece = self.board[coord1[0]][coord1[1]]
    #     if piece.get_player() != player:
    #         return False, 'That is not your piece'

    #     if self.board[coord2[0]][coord2[1]] != 0:
    #         piece2 = self.board[coord2[0]][coord2[1]]
    #         if piece2.get_value() == -1:
    #             return False, 'Cannot move into a lake'
    #         if player == piece2.get_player():
    #             return False, 'You cant move into your own piece'
    #     return True, 'legal move'


    # def get_visible_board(self, player):
    #     visible_board = deepcopy(self.board)
    #     piece_options = []
    #     for x in range(len(self.board)):
    #         for y in range(len(self.board)):
    #             piece = visible_board[x][y]
    #             if piece and piece.player != player and not piece.visible:
    #                 visible_board[x][y].value = 0
    #                 piece_options.append(piece.value)
    #     return visible_board, piece_options



    # Takes in 2 players and returns 0 for p1 winning and 1 for p2 winning, 2 for tie.
    # Also reveals.
    # def battle(self, p1, p2):
    #     v1 = p1.get_value()
    #     v2 = p2.get_value()

    #     p1.reveal()
    #     p2.reveal()

    #     if v1 == 0:
    #         return 1

    #     if v2 == 0:
    #         return 0

    #     if v1 == 10:
    #         if v2 == 8:
    #             return 1
    #         return 0

    #     if v2 == 10:
    #         if v1 == 8:
    #             return 0
    #         return 1

    #     if v1 == 11:
    #         if v2 == 1:
    #             return 0
    #         return 1

    #     if v2 == 11:
    #         if v1 == 1:
    #             return 1
    #         return 0

    #     if v1 == v2:
    #         return 2

    #     if v1 < v2:
    #         return 0
    #     if v1 > v2:
    #         return 1

    #     raise Exception('A case that was not thought of happened')
    #     return False


    # Takes in coord1 [x1, y1] and coord2 [x2, y2]
    # This assumes check_legal has been run.
    # The return is whether or not battle() was run
    def move(self, coord1, coord2):
        p1 = self.board[coord1[0]][coord1[1]]
        self.board[coord1[0]][coord1[1]] = 0
        if not isinstance(self.board[coord2[0]][coord2[1]], Piece):
            self.board[coord2[0]][coord2[1]] = p1
            return False

        p2 = self.board[coord2[0]][coord2[1]]
        winner = self.battle(p1, p2)

        if winner == 0:
            self.board[coord2[0]][coord2[1]] = p1
        elif winner == 2:
            self.board[coord2[0]][coord2[1]] = 0

        return True


    # def legal_moves_for_piece(self, loc, player):
    #     if not isinstance(self.board[loc[0]][loc[1]], Piece):
    #         return []
    #     moves = []

    #     speed = self.board[loc[0]][loc[1]].movement
    #     for i in range(1, speed+1):
    #         if loc[0]+i < 0  or loc[0]+i > self.size-1:
    #             break
    #         if self.board[loc[0]+i][loc[1]] != 0:
    #             moves.append((loc[0]+i, loc[1]))
    #             break
    #         moves.append((loc[0]+i, loc[1]))

    #     for i in range(1, speed+1):
    #         if loc[0]-i < 0  or loc[0]-i > self.size-1:
    #             break
    #         if self.board[loc[0]-i][loc[1]] != 0:
    #             moves.append((loc[0]-i, loc[1]))
    #             break
    #         moves.append((loc[0]-i, loc[1]))

    #     for i in range(1, speed+1):
    #         if loc[1]+i < 0  or loc[1]+i > self.size-1:
    #             break
    #         if self.board[loc[0]][loc[1]+i] != 0:
    #             moves.append((loc[0], loc[1]+i))
    #             break
    #         moves.append((loc[0], loc[1]+i))

    #     for i in range(1, speed+1):
    #         if loc[1]-i < 0  or loc[1]-i > self.size-1:
    #             break
    #         if self.board[loc[0]][loc[1]-i] != 0:
    #             moves.append((loc[0], loc[1]-i))
    #             break
    #         moves.append((loc[0], loc[1]-i))

        
    #     final = []
    #     for move in moves:
    #         if self.check_legal(loc, move, player)[0]:
    #             final.append((loc, move))
    #     return final


    def all_legal_moves(self, player):
        return c_moves.all_legal_moves(player, self.board, self.owner)
        # else:
        #     moves = []
        #     for i in range(len(self.board)):
        #         for j in range(len(self.board[i])):
        #             moves += self.legal_moves_for_piece([i,j], player)
        return moves


    # Takes in player to see if stalemate or something, might be able to removed
    # Returns True or False for if game is over, second is for result
    def check_winner(self, player, moves):
        if not self.board[self.flags[0][0]][self.flags[0][1]].get_value() == 0:
            return True, 1
        if not self.board[self.flags[1][0]][self.flags[1][1]].get_value() == 0:
            return True, 0
        if len(moves) == 0:
            if len(self.all_legal_moves(1-player)) == 0:
                return True, 2
            return True, player
        return False, None


    # Returns representation of the board. Only for db storage atm.
    def get_compacted_board_state(self):
        prev = ''
        counter = 1
        whole = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                piece = self.board[i][j]
                if isinstance(piece, Piece):
                    val = piece.get_value()
                    if not val == -1:
                        player = piece.get_player()
                        if player == 0:
                            player = 'W'
                        else:
                            player = 'B'
                        visible = piece.get_visible()
                else:
                    val = 12

                if val == -1:
                    whole.append('L')
                elif val == 12:
                    whole.append('E')
                else:
                    if visible:
                        whole.append(player + 'V' + str(val))
                    else:
                        whole.append(player + str(val))

                # This was compact but it got confusing to code, work on it later
                # if isinstance(piece, Piece):
                #     abbrev = self.board[i][j].get_abbrev()
                #     if abbrev == 'K':
                #         continue
                # else:
                #     abbrev = 'E'

                # if prev == abbrev:
                #     counter += 1
                # else:
                #     if not counter == 1:
                #         whole.append(str(counter) + str(prev))
                #     else:
                #         whole.append(prev)
                #     counter = 1
                #     prev = abbrev

        return ''.join(whole)


    def move_track(self, coord1, coord2):
        p1 = self.board[coord1[0]][coord1[1]]
        self.board[coord1[0]][coord1[1]] = 0
        if not isinstance(self.board[coord2[0]][coord2[1]], Piece):
            self.board[coord2[0]][coord2[1]] = p1
            return p1, 0

        p2 = self.board[coord2[0]][coord2[1]]
        winner = self.battle(p1, p2)

        if winner == 0:
            self.board[coord2[0]][coord2[1]] = p1
        elif winner == 2:
            self.board[coord2[0]][coord2[1]] = 0

        return p1, p2


    # Functions for minimax
    def push_move(self, coord1, coord2):
        p1, p2 = self.move_track(coord1, coord2)
        self.move_history.append((coord1, coord2, p1, p2))


    def pop_move(self):
        c = self.move_history.pop()
        self.board[c[0][0]][c[0][1]] = c[2]
        self.board[c[1][0]][c[1][1]] = c[3]


    




    # Accidently started developing a function that already existed
    # def get_piece_by_coords(coord, player)
    #     msg = 'legal'
    #     if not isinstance(self.board[coord[0]][coord[1]], Piece):
    #         msg = 'No piece there'
    #         return (False, msg)
    #     piece = self.board[coord[0]][coord[1]]
    #     return piece
