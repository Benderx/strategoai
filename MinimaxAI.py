import random
import math
from GameEngine import Piece

class MinimaxAI:
    def __init__(self, player, engine, depth = 1):
        self.engine = engine
        self.player = player
        self.board = engine.get_board()
        self.depth = depth
    

    def minimax(self, depth, alpha, beta, player):
        if depth == 0:
            return self.eval_board()
        moves = self.engine.all_legal_moves(player)
        if len(moves) == 0:
            return 0

        if player == 0:
            v = -math.inf
            for i in moves:
                self.engine.push_move(i[0], i[1])
                v = max(v, self.minimax(depth - 1, alpha, beta, 1))
                alpha = max(alpha, v)
                self.engine.pop_move()
                if beta <= alpha:
                    break
            return v
        elif player == 1:
            v = math.inf
            for i in moves:
                self.engine.push_move(i[0], i[1])
                v = min(v, self.minimax(depth - 1, alpha, beta, 0))
                beta = min(beta, v)
                self.engine.pop_move()
                if beta <= alpha:
                    break
            return v
        else:
            raise Exception('What?')


    def eval_board(self):
        total = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                piece_eval = 0

                p = self.board[i][j]
                if not isinstance(p, Piece):
                    continue
                v = p.get_value()
                player = p.get_player()
                if v == -1:
                    continue
                elif v == 0:
                    piece_eval = 50000
                elif v == 1:
                    piece_eval = 100
                elif v == 2:
                    piece_eval = 90
                elif v == 3:
                    piece_eval = 80
                elif v == 4:
                    piece_eval = 70
                elif v == 5:
                    piece_eval = 60
                elif v == 6:
                    piece_eval = 50
                elif v == 7:
                    piece_eval = 40
                elif v == 8:
                    piece_eval = 30
                elif v == 9:
                    piece_eval = 20
                elif v == 10:
                    piece_eval = 50
                elif v == 11:
                    piece_eval = 60

                if player == 1:
                    piece_eval *= -1

                total += piece_eval
        return total

    def get_move(self):
        moves = self.engine.all_legal_moves(self.player)
        best_move = [0, None]

        if self.player == 0:
            best_move[0] = -math.inf
        else:
            best_move[0] = math.inf

        for i in moves:
            self.engine.push_move(i[0], i[1])
            if self.player == 0:
                v = self.minimax(self.depth, -math.inf, math.inf, 1)
                if v > best_move[0]:
                    best_move[0] = v
                    best_move[1] = i
            else:
                v = self.minimax(self.depth, -math.inf, math.inf, 1)
                if v < best_move[0]:
                    best_move[0] = v
                    best_move[1] = i
            self.engine.pop_move()

        return best_move[1]