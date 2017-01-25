from libc.stdlib cimport malloc, free
cimport numpy as np
DTYPE = np.int


ctypedef np.int DTYPE_t


def check_legal(self, coord1, coord2, player):
    piece = self.board[coord1[0]][coord1[1]]
    if piece.get_player() != player:
        return False

    if self.board[coord2[0]][coord2[1]] != 0:
        piece2 = self.board[coord2[0]][coord2[1]]
        if piece2.get_value() == -1:
            return False
        if player == piece2.get_player():
            return False
    return True


def battle(self, p1, p2):
    v1 = p1.get_value()
    v2 = p2.get_value()

    p1.reveal()
    p2.reveal()

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
    return False

def legal_moves_for_piece(self, np.ndarray board, np.ndarray owner, cint val, cint player, np.ndarray moves):
    if val == -1 or val == 0:
        return

    cint speed = 1
    if val == 1
    for i in range(1, speed+1):
        if loc[0]+i < 0  or loc[0]+i > self.size-1:
            break
        if self.board[loc[0]+i][loc[1]] != 0:
            moves.append((loc[0]+i, loc[1]))
            break
        moves.append((loc[0]+i, loc[1]))

    for i in range(1, speed+1):
        if loc[0]-i < 0  or loc[0]-i > self.size-1:
            break
        if self.board[loc[0]-i][loc[1]] != 0:
            moves.append((loc[0]-i, loc[1]))
            break
        moves.append((loc[0]-i, loc[1]))

    for i in range(1, speed+1):
        if loc[1]+i < 0  or loc[1]+i > self.size-1:
            break
        if self.board[loc[0]][loc[1]+i] != 0:
            moves.append((loc[0], loc[1]+i))
            break
        moves.append((loc[0], loc[1]+i))

    for i in range(1, speed+1):
        if loc[1]-i < 0  or loc[1]-i > self.size-1:
            break
        if self.board[loc[0]][loc[1]-i] != 0:
            moves.append((loc[0], loc[1]-i))
            break
        moves.append((loc[0], loc[1]-i))

    
    final = []
    for move in moves:
        if self.check_legal(loc, move, player)[0]:
            final.append((loc, move))
    return final


def all_legal_moves(self, player, np.ndarray board, np.ndarray owner):
    cdef np.ndarray moves = np.zeros([0, 150], dtype=DTYPE)
    cint val = 0

    for i in range(board.size):
        c_i = i % board.size
        c_j = (i // board.size)
        val = board[c_i + board.size*c_j]
        legal_moves_for_piece(board, owner, val, player, moves)
    return moves