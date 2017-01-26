from libc.stdlib cimport malloc, free
from libc.math cimport sqrt as sqrt
import numpy as np
cimport numpy as np
DTYPE = np.int8
cimport cython

np.import_array()

ctypedef np.int8_t DTYPE_t


@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef int check_legal(DTYPE_t *board, DTYPE_t *owner, int size, int x, int y, int player, DTYPE_t *moves):
    if player == owner[x + size*y]:
        return 0
    return 1


@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef int legal_moves_for_piece(DTYPE_t *board, DTYPE_t *owner, int size, int val, int x, int y, int player, DTYPE_t *moves, int counter):
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

    cdef int p = 0


    for p in range(speed):
        i = p + 1
        if x+i < 0  or x+i > size-1:
            break

        if board[(x+i) + size*y] == -1:
            break
        elif board[(x+i) + size*y] != 0:
            if check_legal(board, owner, size, x+i, y, player, moves) == 1:
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

    p = 0

    for p in range(speed):
        i = p + 1
        if x-i < 0  or x-i > size-1:
            break

        if board[(x-i) + size*y] == -1:
            break
        elif board[(x-i) + size*y] != 0:
            if check_legal(board, owner, size, x-i, y, player, moves) == 1:
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

    p = 0

    for p in range(speed):
        i = p + 1
        if y+i < 0  or y+i > size-1:
            break

        if board[x + size*(y+i)] == -1:
            break
        elif board[x + size*(y+i)] != 0:
            if check_legal(board, owner, size, x, y+i, player, moves) == 1:
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

    p = 0

    for p in range(speed):
        i = p + 1
        if y-i < 0  or y-i > size-1:
            break

        if board[x + size*(y-i)] == -1:
            break
        elif board[x + size*(y-i)] != 0:
            if check_legal(board, owner, size, x, y-i, player, moves) == 1:
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



@cython.cdivision(True)
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef all_legal_moves(int player, DTYPE_t *board, DTYPE_t *owner, DTYPE_t *moves):
    cdef int g = 0
    for g in range(moves.shape[0]):
        moves[g] = 0


    cdef int truesize = <int>sqrt(board.shape[0])
    cdef int val = 0
    cdef int counter = 1
    cdef int i = 0
    cdef int c_x = 0
    cdef int c_y = 0

    for i in range(board.shape[0]):
        c_x = i % truesize
        c_y = i / truesize
        val = board[c_x + truesize*c_y]
        counter = legal_moves_for_piece(board, owner, truesize, val, c_x, c_y, player, moves, counter)
    moves[0] = (counter-1) / 4



@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef int battle(int v1, int v2):
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
cdef move_piece(int move, DTYPE_t *all_moves, DTYPE_t *board, DTYPE_t *visible, DTYPE_t *owner, int size):
    cdef int x1 = all_moves[(move*4)+1] - 1
    cdef int y1 = all_moves[(move*4)+2] - 1
    cdef int x2 = all_moves[(move*4)+3] - 1
    cdef int y2 = all_moves[(move*4)+4] - 1



    cdef int p1 = board[x1 + size*y1]
    board[x1 + size*(y1)] = 0

    cdef int p2 = board[x2 + size*y2]

    cdef int winner = 0

    if p2 == 0:
        board[x2 + size*y2] = p1
        visible[x2 + size*y2] = 1
        owner[x2 + size*y2] = owner[x1 + size*y1]
        owner[x1 + size*(y1)] = -1
    else:
        winner = battle(p1, p2)

        if winner == 0:
            board[x2 + size*y2] = p1
            visible[x2 + size*y2] = 0
            owner[x2 + size*y2] = owner[x1 + size*y1]
        elif winner == 2:
            board[x2 + size*y2] = 0
            owner[x2 + size*y2] = -1
        owner[x1 + size*(y1)] = -1



@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef check_winner(DTYPE_t *board, DTYPE_t *moves, DTYPE_t *owner, int flag0, int flag1, int player):
    if not board[flag0] == 12:
        return 2
    if not board[flag1] == 12:
        return 1

    if moves[0] == 0:
        all_legal_moves(1-player, board, owner, moves)
        if moves[0] == 0:
            return 3
        return player + 1
    return 0


cdef extern from "numpy/arrayobject.h":
    void PyArray_ENABLEFLAGS(np.ndarray arr, int flags)


cdef data_to_numpy_array_with_spec(void * ptr, np.npy_intp N, int t):
    cdef np.ndarray[DTYPE_t, ndim=1] arr = np.PyArray_SimpleNewFromData(1, &N, t, ptr)
    PyArray_ENABLEFLAGS(arr, np.NPY_OWNDATA)
    return arr



@cython.cdivision(True)
@cython.boundscheck(False)
def primes(int up_to):
    cdef DTYPE_t k = 0
    cdef DTYPE_t *p = <DTYPE_t *>malloc(up_to * sizeof(DTYPE_t))
    
    while k < up_to:
        p[k] = k
        k += 1

    arr = data_to_numpy_array_with_spec(p, up_to, np.NPY_INT8)
    return arr



cdef fill_boards(DTYPE_t *board, DTYPE_t *visible, DTYPE_t *owner, int *flag0, int *flag1, int player):
    # Rivers
    if board_size == 10:
        board[4 + board_size*2] = -1
        board[5 + board_size*2] = -1
        board[4 + board_size*3] = -1
        board[5 + board_size*3] = -1

        board[4 + board_size*6] = -1
        board[5 + board_size*6]
        board[4 + board_size*7]
        board[5 + board_size*7]
    elif board_size == 6:
        board[2 + board_size*2]
        board[3 + board_size*2]

    cdef int rows = 0

    for i in range(0, 2):
        arr = np.empty([50], dtype=DTYPE)
        arr[0] = 11
        arr[1] = 10
        arr[2] = 9
        arr[3] = 8
        arr[4] = 7
        arr[5] = 6
        arr[6] = 5
        arr[7] = 4
        arr[8] = 3
        arr[9] = 2
        arr[10] = 1
        arr[11] = 0

        if board_size == 10:
            rows = 4
        elif board_size == 6:
            rows = 2
            starting_pieces = [[10, 'Bomb B', 1], [11, 'Spy Y', 1], [9, 'Scout S', 1], [8, 'Miner R', 1], [7, 'Sergeant T', 1], [6, 'Lieutenent L', 1], [5, 'Captain C', 1], [4, 'Major J', 1], [3, 'Colonel O', 1], [2, 'General G', 1], [1, 'Marshall M', 1]]

        rand_arr = np.random.permutation(arr)




@cython.cdivision(True)
@cython.boundscheck(False)
def play_game(int AI1, int AI2, int board_size):
    cdef DTYPE_t *players = <DTYPE_t *>malloc(2 * sizeof(DTYPE_t))
    players[0] = AI1
    players[1] = AI2


    # board setup
    cdef DTYPE_t *board = <DTYPE_t *>malloc(board_size * sizeof(DTYPE_t))
    cdef DTYPE_t *visible = <DTYPE_t *>malloc(board_size * sizeof(DTYPE_t))
    cdef DTYPE_t *owner = <DTYPE_t *>malloc(board_size * sizeof(DTYPE_t))

    cdef DTYPE_t *moves = <DTYPE_t *>malloc(1000 * sizeof(DTYPE_t))


    cdef flag0 *int = malloc(sizeof(int))
    cdef flag1 *int = malloc(sizeof(int))
    
    fill_boards(board, visible, owner, flag0, flag1, board_size)


    cdef int move = 0
    cdef int turn = 0
    cdef int winner = 0
    while True:
        all_legal_moves(turn, board, owner, all_moves)

        winner = check_winner(board, all_moves, owner, flag0, flag1, turn) 
        if winner != 0: 
            break

        # RandomAI
        if players[turn] == 0:
            move = players[turn].get_random_move()

        move_piece(move, all_moves, board, visible, owner, board_size) 
        turn = 1 - turn  
    free(players)
    free(board)
    free(visible)
    free(owner)

    return winner

