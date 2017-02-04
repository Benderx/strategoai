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
        self.board = None
        self.owner = None
        self.visible = None
        self.movement = None
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



    def board_setup(self, results_arr, board_size):
        self.board = numpy.zeros((board_size * board_size,), dtype=numpy.int16)
        self.visible = numpy.zeros((board_size * board_size,), dtype=numpy.int16)
        self.owner = numpy.zeros((board_size * board_size,), dtype=numpy.int16)
        self.movement = numpy.zeros((board_size * board_size,), dtype=numpy.int16)

        for i in range(2, (board_size*board_size)+2):
            self.board[i-2] = results_arr[(i*4)-6]
            self.visible[i-2] = results_arr[(i*4)-5]
            self.owner[i-2] = results_arr[(i*4)-4]
            self.movement[i-2] = results_arr[(i*4)-3]

        return (i*4)-2




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



    def battle(self, v1, v2):
        if v1 == 0:
            return 1
        if v2 == 0:
            return 0
        if v1 == 10:
            if v2 == 8:
                return 1
            return 0
        if v2 == 10:
            if v1 == 8:
                return 0
            return 1
        if v1 == 11:
            if v2 == 1:
                return 0
            return 1
        if v2 == 11:
            if v1 == 1:
                return 1
            return 0
        if v1 == v2:
            return 2
        if v1 < v2:
            return 0
        if v1 > v2:
            return 1
        raise Exception('A case that was not thought of happened')
        return False


    def extender(self, s):
        if len(s) == 1:
            return '00' + s
        elif len(s) == 2:
            return '0' + s
        return s


    # Takes in coord1 [x1, y1] and coord2 [x2, y2]
    # This assumes check_legal has been run.
    # The return is whether or not battle() was run
    def move(self, move_tot, size):
        x1 = move_tot[0] - 1
        y1 = move_tot[1] - 1
        x2 = move_tot[2] - 1
        y2 = move_tot[3] - 1

        if x1 == -1:
            return None, None

        p1 = self.board[x1 + size*y1]
        self.board[x1 + size*(y1)] = 0

        p2 = self.board[x2 + size*y2]

        winner = 0

        if p2 == 0:
            self.board[x2 + size*y2] = p1
            self.visible[x2 + size*y2] = self.visible[x1 + size*y1]
            self.owner[x2 + size*y2] = self.owner[x1 + size*y1]
            self.movement[x2 + size*(y2)] = self.movement[x1 + size*(y1)] + 1
        else:
            winner = self.battle(p1, p2)

            if winner == 0:
                self.board[x2 + size*y2] = p1
                self.visible[x2 + size*y2] = 1
                self.owner[x2 + size*y2] = self.owner[x1 + size*y1]
                self.movement[x2 + size*(y2)] = self.movement[x1 + size*(y1)] + 1
            elif winner == 1:
                self.visible[x2 + size*y2] = 1
            elif winner == 2:
                self.board[x2 + size*y2] = 0
                self.owner[x2 + size*y2] = 2
                self.visible[x2 + size*y2] = 0
                self.movement[x2 + size*y2] = 0
        self.visible[x1 + size*y1] = 0
        self.owner[x1 + size*(y1)] = 2
        self.movement[x1 + size*y1] = 0



        return x1 + size*(y1), x2 + size*(y2)
