from libc.stdlib cimport malloc, free
import numpy as np
cimport numpy as np
DTYPE = np.int


ctypedef np.int DTYPE_t


cdef check_legal(np.ndarray board, np.ndarray owner, int x, int y, int player, np.ndarray moves):
    if board[x + board.size*y] == -1:
        return False
    if player == owner[x + board.size*y]:
        return False
    return True


cdef legal_moves_for_piece(np.ndarray board, np.ndarray owner, int size, int val, int x, int y, int player, np.ndarray moves):
    if val == -1 or val == 0:
        return
    if player != owner[x + size*y]:
        return 

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
            if check_legal(board, owner, x+i, y, player, moves):
                moves.append(x+i)
                moves.append(y)
            break

        moves.append(x+i)
        moves.append(y)

    for i in range(1, speed+1):
        if x-i < 0  or x-i > size-1:
            break

        if board[(x-i) + size*y] == -1:
            break
        elif board[(x-i) + size*y] != 0:
            if check_legal(board, owner, x-i, y, player, moves):
                moves.append(x-i)
                moves.append(y)
            break
    
        moves.append(x-i)
        moves.append(y)

    for i in range(1, speed+1):
        if y+i < 0  or y+i > size-1:
            break

        if board[x + size*(y+1)] == -1:
            break
        elif board[x + size*(y+1)] != 0:
            if check_legal(board, owner, x, y+1, player, moves):
                moves.append(x)
                moves.append(y+i)
            break
        
        moves.append(x)
        moves.append(y+i)

    for i in range(1, speed+1):
        if y-i < 0  or y-i > size-1:
            break

        if board[x + size*(y-1)] == -1:
            break
        elif board[x + size*(y-1)] != 0:
            if check_legal(board, owner, x, y-1, player, moves):
                moves.append(x)
                moves.append(y-i)
            break

        moves.append(x)
        moves.append(y-i)

    return


def all_legal_moves(int player, int truesize, np.ndarray board, np.ndarray owner):
    cdef np.ndarray moves = np.zeros([0, 400], dtype=DTYPE)
    cdef int val = 0

    for i in range(board.size):
        c_x = i % truesize
        c_y = i // truesize
        print(c_x, c_y, truesize)
        val = board[c_x + truesize*c_y]
        legal_moves_for_piece(board, owner, truesize, val, c_x, c_y, player, moves)
    return moves