from libc.stdlib cimport malloc, free
import numpy as np
cimport numpy as np
DTYPE = np.int


ctypedef np.int DTYPE_t


cdef check_legal(np.ndarray board, np.ndarray owner, int size, int x, int y, int player, np.ndarray moves):
    if board[x + size*y] == -1:
        return False
    if player == owner[x + size*y]:
        return False
    return True


cdef int legal_moves_for_piece(np.ndarray board, np.ndarray owner, int size, int val, int x, int y, int player, np.ndarray moves, int counter):
    if val == -1 or val == 0:
        return counter
    if player != owner[x + size*y]:
        return counter

    cdef int speed = 1
    if val == 9:
        speed = size
    elif val == 10 or val == 12:
        speed = 0


    for i in range(1, speed+1):
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

    for i in range(1, speed+1):
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

    for i in range(1, speed+1):
        if y+i < 0  or y+i > size-1:
            break

        if board[x + size*(y+1)] == -1:
            break
        elif board[x + size*(y+1)] != 0:
            if check_legal(board, owner, size, x, y+1, player, moves):
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

    for i in range(1, speed+1):
        if y-i < 0  or y-i > size-1:
            break

        if board[x + size*(y-1)] == -1:
            break
        elif board[x + size*(y-1)] != 0:
            if check_legal(board, owner, size, x, y-1, player, moves):
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
    return counter


def all_legal_moves(int player, int truesize, np.ndarray board, np.ndarray owner):
    cdef np.ndarray moves = np.zeros([401], dtype=DTYPE)
    cdef int val = 0
    cdef counter = 1

    for i in range(board.size):
        c_x = i % truesize
        c_y = i // truesize
        val = board[c_x + truesize*c_y]
        counter = legal_moves_for_piece(board, owner, truesize, val, c_x, c_y, player, moves, counter)
    moves[0] = (counter-1) / 4
    return moves