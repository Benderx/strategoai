import math
import random
import inspect
import numpy
from copy import deepcopy
import c_bindings.engine_commands as c_bindings
import time


class GameEngine:
    def __init__(self, n):
        self.size = n
        self.board = numpy.zeros((n * n,), dtype=numpy.int8)
        self.owner = numpy.zeros((n * n,), dtype=numpy.int8)
        self.visible = numpy.zeros((n * n,), dtype=numpy.int8)
        self.moves = numpy.zeros((401), dtype=numpy.int8)
        self.flags = [-1, -1]
        self.move_history = []


    def convert_to_numpy_1D(self, b, b2):
        for x in range(self.size):
            for y in range(self.size):
                b2[y + (self.size * x)] = b[x][y]


    def get_2D_array(self, b):
        board_temp = [[0 for x in range(0, self.size)] for x in range(0, self.size)]
        for x in range(self.size):
            for y in range(self.size):
                board_temp[x][y] = b[x + (self.size * y)]
        return board_temp


    def board_setup(self):
        owner_temp = [[-1 for x in range(0, self.size)] for x in range(0, self.size)]
        visibility_temp = [[0 for x in range(0, self.size)] for x in range(0, self.size)]
        board_temp = [[0 for x in range(0, self.size)] for x in range(0, self.size)]

        # Rivers
        if self.size == 10:
            board_temp[4][2] = -1
            board_temp[5][2] = -1
            board_temp[4][3] = -1
            board_temp[5][3] = -1

            board_temp[4][6] = -1
            board_temp[5][6] = -1
            board_temp[4][7] = -1
            board_temp[5][7] = -1
        elif self.size == 6:
            board_temp[2][2] = -1
            board_temp[3][2] = -1

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
                        owner_temp[y][x] = 0
                        board_temp[y][x] = 12
                        self.flags[0] = x + (self.size * y)
                        starting_pieces.pop(0)
                        continue
                    if y == rows + i*(self.size-rows)-1 and x == randy2 and i == 1:
                        owner_temp[y][x] = 1
                        board_temp[y][x] = 12
                        self.flags[1] = x + (self.size * y)
                        starting_pieces.pop(0)
                        continue
                    starting_locations.append((x, y, i))

            while len(starting_pieces) != 0:
                r1 = int(random.random()*(len(starting_pieces)))
                r2 = int(random.random()*(len(starting_locations)))

                owner_temp[starting_locations[r2][1]][starting_locations[r2][0]] = starting_locations[r2][2]
                board_temp[starting_locations[r2][1]][starting_locations[r2][0]] = starting_pieces[r1][0]

                starting_locations.pop(r2)
                starting_pieces[r1][2] -= 1
                if starting_pieces[r1][2] == 0:
                    starting_pieces.pop(r1)
        self.convert_to_numpy_1D(board_temp, self.board)
        self.convert_to_numpy_1D(owner_temp, self.owner)
        self.convert_to_numpy_1D(visibility_temp, self.visible)



    def print_board(self):
        board_to_print = self.get_2D_array(self.board)
        # owner_board = self.get_2D_array(self.owner)
        print()
        for x in range(self.size):
            arr_temp = []
            for y in range(self.size):
                if board_to_print[x][y]:
                    val = board_to_print[x][y]
                    if val == 12:
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




    # Takes in coord1 [x1, y1] and coord2 [x2, y2]
    # This assumes check_legal has been run.
    # The return is whether or not battle() was run
    def move(self, move):
        c_bindings.move(move, self.moves, self.board, self.visible, self.owner, self.size)
        return


    def all_legal_moves(self, player):
        # timing_total = 0
        # timing_samples = 0

        # for i in range(0, 100):
        #     start = time.perf_counter()
        #     c_bindings.primes(i)
        #     end = time.perf_counter()
        #     timing_total += end-start
        #     timing_samples += 1

        # print("avg:", timing_total/timing_samples)
        # exit()


        return c_bindings.all_legal_moves(player, self.board, self.owner, self.moves)


    # Takes in player to see if stalemate or something, might be able to removed
    # Returns True or False for if game is over, second is for result
    def check_winner(self, player):
        return c_bindings.check_winner(self.board, self.moves, self.owner, self.flags[0], self.flags[1], player)


    # Returns representation of the board. Only for db storage atm.
    def get_compacted_board_state(self):
        prev = ''
        counter = 1
        whole = []
        board = self.get_2D_array(self.board)
        owner = self.get_2D_array(self.owner)
        visible = self.get_2D_array(self.visible)
        for i in range(len(board)):
            for j in range(len(board[i])):
                val = board[j][i]
                if val != 0 and val != -1:
                    player = owner[j][i]
                    if player == 0:
                        player = 'W'
                    else:
                        player = 'B'
                    v = visible[j][i]

                if val == -1:
                    whole.append('L')
                elif val == 12:
                    whole.append('F')
                elif val == 0:
                    whole.append('0')
                else:
                    if v:
                        whole.append(player + 'V' + str(val))
                    else:
                        whole.append(player + str(val))
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

