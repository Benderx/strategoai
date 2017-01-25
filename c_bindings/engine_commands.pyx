from libc.stdlib cimport malloc, free
from libc.math cimport sqrt as sqrt
import numpy as np
cimport numpy as np
DTYPE = np.int8
cimport cython


ctypedef np.int8_t DTYPE_t


@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef check_legal(np.ndarray[DTYPE_t] board, np.ndarray[DTYPE_t] owner, int size, int x, int y, int player, np.ndarray[DTYPE_t] moves):
    if player == owner[x + size*y]:
        return False
    return True


@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef int legal_moves_for_piece(np.ndarray[DTYPE_t] board, np.ndarray[DTYPE_t] owner, int size, int val, int x, int y, int player, np.ndarray[DTYPE_t] moves, int counter):
    if val == -1 or val == 0:
        return counter
    if player != owner[x + size*y]:
        return counter

    cdef int speed = 1
    cdef int i = 0
    if val == 9:
        speed = size
    elif val == 10 or val == 12:
        speed = 0


    for p in range(speed):
        i = p + 1
        if x+i < 0  or x+i > size-1:
            break

        if board[(x+i) + size*y] == -1:
            break
        elif board[(x+i) + size*y] != 0:
            if check_legal(board, owner, size, x+i, y, player, moves):
                moves[counter] = x + 1
                moves[counter+1] = y + 1
                moves[counter+2] = x+i + 1
                moves[counter+3] = y + 1
                counter += 4
            break

        moves[counter] = x + 1
        moves[counter+1] = y + 1
        moves[counter+2] = x+i + 1
        moves[counter+3] = y + 1
        counter += 4

    for p in range(speed):
        i = p + 1
        if x-i < 0  or x-i > size-1:
            break

        if board[(x-i) + size*y] == -1:
            break
        elif board[(x-i) + size*y] != 0:
            if check_legal(board, owner, size, x-i, y, player, moves):
                moves[counter] = x + 1
                moves[counter+1] = y + 1
                moves[counter+2] = x-i + 1
                moves[counter+3] = y + 1
                counter += 4
            break
    
        moves[counter] = x + 1
        moves[counter+1] = y + 1
        moves[counter+2] = x-i + 1
        moves[counter+3] = y + 1
        counter += 4

    for p in range(speed):
        i = p + 1
        if y+i < 0  or y+i > size-1:
            break

        if board[x + size*(y+i)] == -1:
            break
        elif board[x + size*(y+i)] != 0:
            if check_legal(board, owner, size, x, y+i, player, moves):
                moves[counter] = x + 1
                moves[counter+1] = y + 1
                moves[counter+2] = x + 1
                moves[counter+3] = y+i + 1
                counter += 4
            break
        
        moves[counter] = x + 1
        moves[counter+1] = y + 1
        moves[counter+2] = x + 1
        moves[counter+3] = y+i + 1
        counter += 4

    for p in range(speed):
        i = p + 1
        if y-i < 0  or y-i > size-1:
            break

        if board[x + size*(y-i)] == -1:
            break
        elif board[x + size*(y-i)] != 0:
            if check_legal(board, owner, size, x, y-i, player, moves):
                moves[counter] = x + 1
                moves[counter+1] = y + 1
                moves[counter+2] = x + 1
                moves[counter+3] = y-i + 1
                counter += 4
            break

        moves[counter] = x + 1
        moves[counter+1] = y + 1
        moves[counter+2] = x + 1
        moves[counter+3] = y-i + 1
        counter += 4
    # print(x, y, val)
    # print(counter)
    # print(moves)
    return counter



@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def all_legal_moves(int player, np.ndarray[DTYPE_t] board, np.ndarray[DTYPE_t] owner):
    cdef int truesize = <int>sqrt(board.shape[0])
    cdef np.ndarray moves = np.zeros([401], dtype=DTYPE)
    cdef int val = 0
    cdef counter = 1

    for i in range(board.shape[0]):
        c_x = i % truesize
        c_y = i // truesize
        val = board[c_x + truesize*c_y]
        counter = legal_moves_for_piece(board, owner, truesize, val, c_x, c_y, player, moves, counter)
    moves[0] = (counter-1) / 4
    return moves



@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef int battle(v1, v2):
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
    return -1



@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def move(int move, np.ndarray[DTYPE_t] all_moves, np.ndarray[DTYPE_t] board, np.ndarray[DTYPE_t] visible, np.ndarray[DTYPE_t] owner, int size):
    cdef int x1 = all_moves[(move*4)+1] - 1
    cdef int y1 = all_moves[(move*4)+2] - 1
    cdef int x2 = all_moves[(move*4)+3] - 1
    cdef int y2 = all_moves[(move*4)+4] - 1



    p1 = board[x1 + size*y1]
    board[x1 + size*(y1)] = 0

    p2 = board[x2 + size*y2]

    if p2 == 0:
        board[x2 + size*y2] = p1
        visible[x2 + size*y2] = 1
        owner[x2 + size*y2] = owner[x1 + size*y1]
        owner[x1 + size*(y1)] = -1
        return

    winner = battle(p1, p2)

    if winner == 0:
        board[x2 + size*y2] = p1
        visible[x2 + size*y2] = 0
        owner[x2 + size*y2] = owner[x1 + size*y1]
    elif winner == 2:
        board[x2 + size*y2] = 0
        owner[x2 + size*y2] = -1
    owner[x1 + size*(y1)] = -1
    return



@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def check_winner(np.ndarray[DTYPE_t] board, np.ndarray[DTYPE_t] moves, np.ndarray[DTYPE_t] owner, int flag0, int flag1, int player):
    if not board[flag0] == 12:
        return 2
    if not board[flag1] == 12:
        return 1

    if moves[0] == 0:
        if all_legal_moves(1-player, board, owner)[0] == 0:
            return 3
        return player + 1
    return 0
