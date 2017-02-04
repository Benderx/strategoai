from libc.stdlib cimport malloc, free, rand, srand, RAND_MAX
from libc.math cimport sqrt as sqrt
cimport cython
cimport numpy as np

import numpy as np
import time


DTYPE = np.int16
np.import_array()

ctypedef np.int16_t DTYPE_t

cdef extern from "limits.h":
    int INT_MAX

cdef extern from "numpy/arrayobject.h":
    void PyArray_ENABLEFLAGS(np.ndarray arr, int flags)



@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef int check_legal(DTYPE_t *board, DTYPE_t *owner, int size, int x, int y, int player, DTYPE_t *moves):
    if player == owner[x + size*y]:
        return 0
    return 1


@cython.cdivision(True)
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef int legal_square_for_piece(DTYPE_t *board, DTYPE_t *owner, int size, int val, int old_x, int old_y, int new_x, int new_y, int player, DTYPE_t *moves, int *counter, int speed):
    if board[new_x + size*new_y] == 0:
        moves[counter[0]] = old_x + 1
        moves[counter[0]+1] = old_y + 1
        moves[counter[0]+2] = new_x + 1
        moves[counter[0]+3] = new_y + 1
        counter[0] += 4
        return 0
        # return 0 # no break, increment
    elif board[new_x + size*new_y] == 13:
        return 1 # break proccess no increment
    elif board[new_x + size*new_y] != 0:
        if check_legal(board, owner, size, new_x, new_y, player, moves) == 1:
            moves[counter[0]] = old_x + 1
            moves[counter[0]+1] = old_y + 1
            moves[counter[0]+2] = new_x + 1
            moves[counter[0]+3] = new_y + 1
            counter[0] += 4
            # return 2 # break proccess increment
        return 1


@cython.cdivision(True)
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef void legal_moves_for_piece(DTYPE_t *board, DTYPE_t *owner, int size, int val, int x, int y, int player, DTYPE_t *moves, int *counter):
    # if val == 13 or val == 0:
    #     return counter
    if player != owner[x + size*y]:
        return
    cdef int speed = 1

    if val == 9:
        speed = size
    elif val == 10 or val == 12:
        return

    cdef int p = 0
    cdef int i
    cdef int new_x
    cdef int new_y

    for p in range(speed):
        i = p + 1
        new_x = x+i

        if new_x < 0  or new_x > size-1:
            break

        if legal_square_for_piece(board, owner, size, val, x, y, new_x, y, player, moves, counter, speed):
            break
        # if ret == 0:
        #     counter += 4
        # elif ret == 1:
        #     break
        # elif ret == 2:
        #     counter += 4
        #     break
        # elif ret == 4:
        #     print("plz no")

    p = 0
    for p in range(speed):
        i = p + 1
        new_x = x-i

        if new_x < 0  or new_x > size-1:
            break

        if legal_square_for_piece(board, owner, size, val, x, y, new_x, y, player, moves, counter, speed):
            break
        # if ret == 0:
        #     counter += 4
        # elif ret == 1:
        #     break
        # elif ret == 2:
        #     counter += 4
        #     break
        # elif ret == 4:
        #     print("plz no")

    p = 0
    for p in range(speed):
        i = p + 1
        new_y = y+i

        if new_y < 0  or new_y > size-1:
            break

        if legal_square_for_piece(board, owner, size, val, x, y, x, new_y, player, moves, counter, speed):
            break
        # if ret == 0:
        #     counter += 4
        # elif ret == 1:
        #     break
        # elif ret == 2:
        #     counter += 4
        #     break
        # elif ret == 4:
        #     print("plz no")

    p = 0
    for p in range(speed):
        i = p + 1
        new_y = y-i

        if new_y < 0  or new_y > size-1:
            break

        if legal_square_for_piece(board, owner, size, val, x, y, x, new_y, player, moves, counter, speed):
            break
        # if ret == 0:
        #     counter += 4
        # elif ret == 1:
        #     break
        # elif ret == 2:
        #     counter += 4
        #     break
        # elif ret == 4:
        #     print("plz no")



# @cython.cdivision(True)
# @cython.boundscheck(False) # turn off bounds-checking for entire function
# @cython.wraparound(False)  # turn off negative index wrapping for entire function
# cdef int legal_moves_for_piece(DTYPE_t *board, DTYPE_t *owner, int size, int val, int x, int y, int player, DTYPE_t *moves, int counter):
#     # if val == 13 or val == 0:
#     #     return counter
#     if player != owner[x + size*y]:
#         return counter
#     cdef int speed = 1

#     if val == 9:
#         speed = size
#     elif val == 10 or val == 12:
#         return counter

#     cdef int p = 0
#     cdef int i
#     for p in range(speed):
#         i = p + 1
#         if x+i < 0  or x+i > size-1:
#             break

#         if board[(x+i) + size*y] == 0:
#             moves[counter] = x + 1
#             moves[counter+1] = y + 1
#             moves[counter+2] = x+i + 1
#             moves[counter+3] = y + 1
#             counter += 4

#         elif board[(x+i) + size*y] == 13:
#             break
#         elif board[(x+i) + size*y] != 0:
#             if check_legal(board, owner, size, x+i, y, player, moves) == 1:
#                 moves[counter] = x + 1
#                 moves[counter+1] = y + 1
#                 moves[counter+2] = x+i + 1
#                 moves[counter+3] = y + 1
#                 counter += 4
#             break

#     p = 0

#     for p in range(speed):
#         i = p + 1
#         if x-i < 0  or x-i > size-1:
#             break

#         if board[(x-i) + size*y] == 0:
#             moves[counter] = x + 1
#             moves[counter+1] = y + 1
#             moves[counter+2] = x-i + 1
#             moves[counter+3] = y + 1
#             counter += 4

#         elif board[(x-i) + size*y] == 13:
#             break
#         elif board[(x-i) + size*y] != 0:
#             if check_legal(board, owner, size, x-i, y, player, moves) == 1:
#                 moves[counter] = x + 1
#                 moves[counter+1] = y + 1
#                 moves[counter+2] = x-i + 1
#                 moves[counter+3] = y + 1
#                 counter += 4
#             break

#     p = 0

#     for p in range(speed):
#         i = p + 1
#         if y+i < 0  or y+i > size-1:
#             break

#         if board[x + size*(y+i)] == 0:
#             moves[counter] = x + 1
#             moves[counter+1] = y + 1
#             moves[counter+2] = x + 1
#             moves[counter+3] = y+i + 1
#             counter += 4

#         elif board[x + size*(y+i)] == 13:
#             break
#         elif board[x + size*(y+i)] != 0:
#             if check_legal(board, owner, size, x, y+i, player, moves) == 1:
#                 moves[counter] = x + 1
#                 moves[counter+1] = y + 1
#                 moves[counter+2] = x + 1
#                 moves[counter+3] = y+i + 1
#                 counter += 4
#             break

#     p = 0

#     for p in range(speed):
#         i = p + 1
#         if y-i < 0  or y-i > size-1:
#             break

#         if board[x + size*(y-i)] == 0:
#             moves[counter] = x + 1
#             moves[counter+1] = y + 1
#             moves[counter+2] = x + 1
#             moves[counter+3] = y-i + 1
#             counter += 4
#         elif board[x + size*(y-i)] == 13:
#             break
#         elif board[x + size*(y-i)] != 0:
#             if check_legal(board, owner, size, x, y-i, player, moves) == 1:
#                 moves[counter] = x + 1
#                 moves[counter+1] = y + 1
#                 moves[counter+2] = x + 1
#                 moves[counter+3] = y-i + 1
#                 counter += 4
#             break
#     # print(x, y, val)
#     # print(counter)
#     # print(moves)
#     return counter



@cython.cdivision(True)
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef void all_legal_moves(int player, DTYPE_t *board, DTYPE_t *owner, DTYPE_t *moves, int move_size, int board_size):
    cdef int g = 0
    # for g in range(move_size):
    #     moves[g] = 0
    cdef int *counter = <int *>malloc(sizeof(int))
    counter[0] = 1
    # print("legal_enter", counter[0])

    cdef int val = 0
    cdef int i = 0
    cdef int c_x = 0
    cdef int c_y = 0

    for i in range(board_size*board_size):
        c_x = i % board_size
        c_y = i / board_size
        val = board[c_x + board_size*c_y]
        legal_moves_for_piece(board, owner, board_size, val, c_x, c_y, player, moves, counter)
    moves[0] = <int> ((counter[0]-1) / 4)
    free(counter)

    # print("moves", moves[0])
    # for jk in range(moves[0]*4):
    #     print(player, moves[jk+1])
    # time.sleep(1000)



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
cdef void move_piece(int move, DTYPE_t *all_moves, DTYPE_t *board, DTYPE_t *visible, DTYPE_t *owner, int size, DTYPE_t *movement):
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
        visible[x2 + size*y2] = visible[x1 + size*y1]
        owner[x2 + size*y2] = owner[x1 + size*y1]
        movement[x2 + size*(y2)] = movement[x1 + size*(y1)] + 1
    else:
        winner = battle(p1, p2)

        if winner == 0:
            board[x2 + size*y2] = p1
            visible[x2 + size*y2] = 1
            owner[x2 + size*y2] = owner[x1 + size*y1]
            movement[x2 + size*(y2)] = movement[x1 + size*(y1)] + 1
        elif winner == 1:
            visible[x2 + size*y2] = 1
        elif winner == 2:
            board[x2 + size*y2] = 0
            owner[x2 + size*y2] = 2
            visible[x2 + size*y2] = 0
            movement[x2 + size*(y2)] = 0
    visible[x1 + size*y1] = 0
    owner[x1 + size*(y1)] = 2
    movement[x1 + size*(y1)] = 0



@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef int check_winner(DTYPE_t *board, DTYPE_t *moves, DTYPE_t *owner, DTYPE_t *flags, int player, int move_size, int board_size):
    if not board[flags[0]] == 12:
        return 1
    if not board[flags[1]] == 12:
        return 0

    if moves[0] == 0:
        all_legal_moves(1-player, board, owner, moves, move_size, board_size)
        if moves[0] == 0:
            return 2
        return player + 1
    return 3



@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef void set_to(DTYPE_t *to_set, int size, int to):
    cdef int i = 0
    for i in range(size):
        to_set[i] = to


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef void fill_boards(DTYPE_t *board, DTYPE_t *visible, DTYPE_t *owner, DTYPE_t *flags, int board_size):
    # Rivers

    if board_size == 10:
        board[2 + board_size*4] = 13
        board[2 + board_size*5] = 13
        board[3 + board_size*4] = 13
        board[3 + board_size*5] = 13

        board[6 + board_size*4] = 13
        board[6 + board_size*5] = 13
        board[7 + board_size*4] = 13
        board[7 + board_size*5] = 13
    else:
        board[2 + board_size*2] = 13
        board[2 + board_size*3] = 13

    cdef int rows = 0
    cdef int piece_counter = 0
    cdef int i
    cdef int x, y, calc_num

    cdef int rander1 = rand()
    cdef int rander2 = rand()

    # places flags on backrank
    cdef int pos0 = rander1 % board_size
    cdef int pos1 = rander2 % board_size

    board[pos0] = 12
    visible[pos0] = 0
    owner[pos0] = 0

    board[pos1 + board_size*(board_size-1)] = 12
    visible[pos1 + board_size*(board_size-1)] = 0
    owner[pos1 + board_size*(board_size-1)] = 1


    flags[0] = pos0
    flags[1] = pos1 + board_size*(board_size-1)

    cdef int flag0 = pos0
    cdef int flag1 = pos1

    # print(pos0, pos1, rander1, rander2)

    i = 0
    for i in range(0, 2):
        # All piece but flag
        
        if board_size == 10:
            rows = 4
            arr = np.empty([(rows * board_size) - 1], dtype=DTYPE)
            arr[0] = 11
            arr[1] = 10
            arr[2] = 10
            arr[3] = 10
            arr[4] = 10
            arr[5] = 10
            arr[6] = 10
            arr[7] = 9
            arr[8] = 9
            arr[9] = 9
            arr[10] = 9
            arr[11] = 9
            arr[12] = 9
            arr[13] = 9
            arr[14] = 9
            arr[15] = 8
            arr[16] = 8
            arr[17] = 8
            arr[18] = 8
            arr[19] = 8
            arr[20] = 7
            arr[21] = 7
            arr[22] = 7
            arr[23] = 7
            arr[24] = 6
            arr[25] = 6
            arr[26] = 6
            arr[27] = 6
            arr[28] = 5
            arr[29] = 5
            arr[30] = 5
            arr[31] = 5
            arr[32] = 4
            arr[33] = 4
            arr[34] = 4
            arr[35] = 3
            arr[36] = 3
            arr[37] = 2
            arr[38] = 1
            # starting_pieces = [[[11, 'Spy Y', 1], [10, 'Bomb B', 6], [9, 'Scout S', 8], [8, 'Miner R', 5], [7, 'Sergeant T', 4], [6, 'Lieutenent L', 4], [5, 'Captain C', 4], [4, 'Major J', 3], [3, 'Colonel O', 2], [2, 'General G', 1], [1, 'Marshall M', 1]]
        elif board_size == 6:
            rows = 2
            arr = np.empty([(rows * board_size) - 1], dtype=DTYPE)
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
            # starting_pieces = [[11, 'Spy Y', 1], [10, 'Bomb B', 1], [9, 'Scout S', 1], [8, 'Miner R', 1], [7, 'Sergeant T', 1], [6, 'Lieutenent L', 1], [5, 'Captain C', 1], [4, 'Major J', 1], [3, 'Colonel O', 1], [2, 'General G', 1], [1, 'Marshall M', 1]]

        x = 0
        y = 0


        


        rand_arr = np.random.permutation(arr)
        piece_counter = 0

        for x in range(0, board_size):
            for y in range(0 + i*(board_size-rows), rows + i*(board_size-rows)):
                calc_num = x + y*board_size

                if (x == flag0 and y == 0) or (x == flag1 and y == board_size-1):
                    continue
                board[calc_num] = rand_arr[piece_counter]
                visible[calc_num] = 0
                owner[calc_num] = i
                piece_counter += 1



@cython.cdivision(True)
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef int get_random_move(DTYPE_t *all_moves, int move_size):
    return rand() % all_moves[0]


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef void write_init_return_board(np.int16_t *return_stuff, DTYPE_t *board, DTYPE_t *visible, DTYPE_t *owner, DTYPE_t *movement, int board_size, int max_return_size):
    cdef int i = 2
    for i in range(2, (board_size*board_size) + 2):
        return_stuff[(i*4)-6] = board[i-2]
        return_stuff[(i*4)-5] = visible[i-2]
        return_stuff[(i*4)-4] = owner[i-2]
        return_stuff[(i*4)-3] = movement[i-2]


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef void write_return_move(np.int16_t *return_stuff, DTYPE_t *all_moves, int move, int write_counter):
    return_stuff[write_counter] = all_moves[(move*4) + 1]
    return_stuff[write_counter+1] = all_moves[(move*4) + 2]
    return_stuff[write_counter+2] = all_moves[(move*4) + 3]
    return_stuff[write_counter+3] = all_moves[(move*4) + 4]


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef int monte_sample(DTYPE_t *board, DTYPE_t *visible, DTYPE_t *owner, DTYPE_t *movement, int board_size, DTYPE_t *flags, DTYPE_t *parent_moves, int parent_move, int turn_parent, DTYPE_t *sample_moves, int move_size):

    move_piece(parent_move, parent_moves, board, visible, owner, board_size, movement) 

    cdef DTYPE_t *players = <DTYPE_t *>malloc(2 * sizeof(DTYPE_t))
    players[0] = 0
    players[1] = 0

    # set_to(sample_moves, move_size, 0)

    cdef int num_moves = 0
    cdef float time_tot = 0
    cdef float start
    cdef float end

    cdef int move = 0
    cdef int turn = 1 - turn_parent
    cdef int winner = 0


    while True:
        start = time.perf_counter()
        all_legal_moves(turn, board, owner, sample_moves, move_size, board_size)
        end = time.perf_counter()

        winner = check_winner(board, sample_moves, owner, flags, turn, move_size, board_size) 
        if winner != 3: 
            break

        # RandomAI
        move = get_random_move(sample_moves, move_size)

        move_piece(move, sample_moves, board, visible, owner, board_size, movement) 

        time_tot += (end - start)
        num_moves += 1
        turn = 1 - turn 
    
    print('Time:', time_tot/num_moves)

    free(players)

    if winner == turn_parent:
        return 2
    # if winner == 2:
    #     return 1

    # print('Time:', (end - start), end, start)
    return 0


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef void copy_arr(DTYPE_t *arr_empty, DTYPE_t *arr_copy, int size):
    cdef int i = 0
    for i in range(size):
        arr_empty[i] = arr_copy[i]


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False) 
cdef void get_unknown_flag_loc(DTYPE_t *unknowns, DTYPE_t *board, DTYPE_t *visible, DTYPE_t *owner, DTYPE_t *movement, int player, int board_size):
    cdef int i = 0
    cdef int counter = 1
    for i in range((1-player) * (board_size-1), (1-player) * (board_size-1) + board_size):
        if owner[i] == (1-player) and visible[i] == 0 and movement[i] == 0:
            unknowns[counter] = i
            counter += 1
    unknowns[0] = counter-1


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False) 
cdef int get_bombs_left(DTYPE_t *board, DTYPE_t *visible, DTYPE_t *owner, int player, int board_size):
    cdef int i = 0
    cdef int counter = 1
    for i in range((1-player) * (board_size-1), (1-player) * (board_size-1) + board_size):
        if owner[i] == (1-player) and visible[i] == 0 and board[i] == 10:
            counter += 1
    return counter



@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False) 
cdef void get_unknown_pieces(DTYPE_t *unknowns, DTYPE_t *board, DTYPE_t *visible, DTYPE_t *owner, int player, int board_size, int new_flag_loc):
    cdef int i = 0
    cdef int counter = 1
    for i in range(0, board_size * board_size):
        if board[i] == 12:
            continue
        if owner[i] == (1-player) and visible[i] == 0:
            unknowns[counter] = board[i]
            counter += 1
    unknowns[0] = counter-1


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False) 
cdef int get_randomized_board(DTYPE_t *sample_board, DTYPE_t *board, DTYPE_t *visible, DTYPE_t *owner, DTYPE_t *movement, int board_size, int player, DTYPE_t *unknowns, DTYPE_t *unknown_mixed):
    cdef int i = 0
    cdef int counter = 1
    cdef int new_flag_loc = 0

    get_unknown_flag_loc(unknowns, board, visible, owner, movement, player, board_size)
    if unknowns[0] == 0:
        print("something went terribly wrong, get_randomized_board()")

    new_flag_loc = unknowns[(rand() % unknowns[0])+1]


    cdef int num_bombs = get_bombs_left(board, visible, owner, player, board_size)
    get_unknown_pieces(unknowns, board, visible, owner, player, board_size, new_flag_loc)


    # GEN ALL OTHER LOCATIONS
    cdef int n = unknowns[0]
    while n > 0:
        # use rand to generate a random number x in the range 0..n-1
        x = (rand() % n)+1
        # add source_array[x] to the result list
        unknown_mixed[unknowns[0]-n+1] = unknowns[x]
        # source_array[x] = source_array[n-1]; // replace number just used with last value
        unknowns[x] = unknowns[n]
        n -= 1
    

    # PLACE ALL OTHERS
    i = 0
    n = 0
    for i in range(board_size * board_size):
        if i == new_flag_loc:
            continue
        if owner[i] != (1-player) or visible[i] == 1:
            sample_board[i] = board[i]
        else:
            if counter-1 < num_bombs:
                sample_board[i] = 10
            else:
                sample_board[i] = unknown_mixed[counter]
            counter += 1

    sample_board[new_flag_loc] = 12
    return new_flag_loc



@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cdef int get_monte_move(DTYPE_t *board, DTYPE_t *visible, DTYPE_t *owner, DTYPE_t *movement, DTYPE_t *sample_board, DTYPE_t *sample_visible, DTYPE_t *sample_owner, DTYPE_t *sample_movement, int monte_samples, int board_size, DTYPE_t *all_moves, DTYPE_t *flags, int turn, DTYPE_t *unknowns, DTYPE_t *unknown_mixed, DTYPE_t *sample_moves, int move_size):
    cdef int i = 0
    cdef int value = 0      
    cdef int flag_store = 0
    cdef int new_flag = 0

    cdef float *move_ratings = <float *>malloc(all_moves[0] * sizeof(float))
    cdef float *move_samples = <float *>malloc(all_moves[0] * sizeof(float))

    for i in range(all_moves[0]):
        move_ratings[i] = -1
        i = 0
    for i in range(all_moves[0]):
        move_samples[i] = 1

    i = 0
    # moves_copy = all_moves.copy()

    while i < monte_samples:
        move = i%all_moves[0]



        # Does visibility matter?
        new_flag = get_randomized_board(sample_board, board, visible, owner, movement, board_size, turn, unknowns, unknown_mixed)
        copy_arr(sample_visible, visible, board_size * board_size)
        copy_arr(sample_owner, owner, board_size * board_size)
        copy_arr(sample_movement, movement, board_size * board_size)

        flag_store = flags[1-turn]
        flags[1-turn] = new_flag
        # start = time.perf_counter()
        value = monte_sample(sample_board, sample_visible, sample_owner, sample_movement, board_size, flags, all_moves, move, turn, sample_moves, move_size)
        # end = time.perf_counter()
        # print('Time:', end - start)

        flags[1-turn] = flag_store
        if move_ratings[move] != -1:
            move_ratings[move] = move_ratings[move]*move_samples[move]/(move_samples[move]+1) + value / (move_samples[move] + 1)
            move_samples[move] += 1
        else:
            move_ratings[move] = value   
        i+=1

    i = 0
    cdef float max_num = move_ratings[0]
    cdef int max_index = 0
    for i in range(1, all_moves[0]):
        if move_ratings[i] > max_num:
            max_num = move_ratings[i]
            max_index = i

    free(move_ratings)
    free(move_samples)
    return max_index




@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def play_game(int AI1, int AI2, int monte_samples, int board_size):

    srand(int(np.random.rand()*100000))
    cdef DTYPE_t *players = <DTYPE_t *>malloc(2 * sizeof(DTYPE_t))
    players[0] = AI1
    players[1] = AI2

    cdef int move_size = 10001 # (number of possible moves (1000) * 4) + 1
    cdef int max_return_size = 400002 # (max moves in a game (5000) * 4) + 2

    # MONTE STUFF
    cdef int unknown_size = 6001

    # board setup
    cdef DTYPE_t *board = <DTYPE_t *>malloc(board_size * board_size * sizeof(DTYPE_t))
    cdef DTYPE_t *visible = <DTYPE_t *>malloc(board_size * board_size * sizeof(DTYPE_t))
    cdef DTYPE_t *owner = <DTYPE_t *>malloc(board_size * board_size * sizeof(DTYPE_t))
    cdef DTYPE_t *movement = <DTYPE_t *>malloc(board_size * board_size * sizeof(DTYPE_t))

    cdef DTYPE_t *all_moves = <DTYPE_t *>malloc(move_size * sizeof(DTYPE_t))
    cdef DTYPE_t *sample_moves = <DTYPE_t *>malloc(move_size * sizeof(DTYPE_t))

    cdef DTYPE_t *unknowns = <DTYPE_t *>malloc(unknown_size * sizeof(DTYPE_t))
    cdef DTYPE_t *unknown_mixed = <DTYPE_t *>malloc(unknown_size * sizeof(DTYPE_t))


    # Initilizing return_stuff
    cdef np.int16_t *return_stuff = <np.int16_t *>malloc(max_return_size * sizeof(np.int16_t))
    cdef int i = 0
    for i in range(max_return_size):
        return_stuff[i] = 0


    # ONLY FOR MONTE
    cdef DTYPE_t *sample_board = <DTYPE_t *>malloc(board_size * board_size * sizeof(DTYPE_t))
    cdef DTYPE_t *sample_visible = <DTYPE_t *>malloc(board_size * board_size * sizeof(DTYPE_t))
    cdef DTYPE_t *sample_owner = <DTYPE_t *>malloc(board_size * board_size * sizeof(DTYPE_t))
    cdef DTYPE_t *sample_movement = <DTYPE_t *>malloc(board_size * board_size * sizeof(DTYPE_t))


    set_to(board, board_size*board_size, 0)
    set_to(visible, board_size*board_size, 0)
    set_to(owner, board_size*board_size, 2)
    set_to(movement, board_size*board_size, 0)
    set_to(all_moves, move_size, 0)
    set_to(unknowns, unknown_size, 0)
    set_to(unknown_mixed, unknown_size, 0)
    

    cdef  DTYPE_t *flags = <DTYPE_t *>malloc(2 * sizeof(DTYPE_t))
    fill_boards(board, visible, owner, flags, board_size)

    # print(flags[0])
    # print(flags[1])


    write_init_return_board(return_stuff, board, visible, owner, movement, board_size, max_return_size)

    cdef int write_counter = (board_size * board_size * 4) + 2

    cdef int move = 0
    cdef int turn = 0
    cdef int winner = 0
    cdef int num_moves = 0
    while True:
        all_legal_moves(turn, board, owner, all_moves, move_size, board_size)

        winner = check_winner(board, all_moves, owner, flags, turn, move_size, board_size) 
        if winner != 3: 
            break

        # RandomAI
        if players[turn] == 0:
            move = get_random_move(all_moves, move_size)
        elif players[turn] == 1:
            move = get_monte_move(board, visible, owner, movement, sample_board, sample_visible, sample_owner, sample_movement, monte_samples, board_size, all_moves, flags, turn, unknowns, unknown_mixed, sample_moves, move_size)
            # print('moved for real')
            # time.sleep(100)



        move_piece(move, all_moves, board, visible, owner, board_size, movement) 
        write_return_move(return_stuff, all_moves, move, write_counter)
        write_counter += 4

        # print("move", num_moves)

        num_moves += 1
        turn = 1 - turn 
    free(players)
    free(board)
    free(visible)
    free(owner)
    free(flags)
    free(all_moves)

    free(sample_board)
    free(sample_visible)
    free(sample_owner)
    free(sample_movement)
    free(sample_moves)

    free(unknowns)
    free(unknown_mixed)

    return_stuff[0] = winner
    return_stuff[1] = num_moves

    cdef int a = 0
    tmp = np.zeros([max_return_size], dtype=np.int16)

    for a in range(max_return_size):
        tmp[a] = return_stuff[a]

    free(return_stuff)
    return tmp

