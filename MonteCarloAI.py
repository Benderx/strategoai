import random
import GameEngine
from copy import deepcopy
import RandomAI
import time
import numpy

TOTAL_SAMPLES = 500

class MonteCarloAI:
    def __init__(self, player, engine, depth = 1):
        self.engine = engine
        self.player = player
        self.trans_table = {} # tbd
        self.type = 1
    

    def get_move(self):
        all_moves = self.engine.moves

        i = 0
        move_ratings = [-1 for x in range(all_moves[0])]
        move_samples = [1 for x in range(all_moves[0])]

        tot_moves = all_moves[0]

        moves_copy = all_moves.copy()

        while i < TOTAL_SAMPLES:
            move = i%tot_moves

            value = self.sample(move)
            if move_ratings[move] != -1:
                move_ratings[move] = move_ratings[move]*move_samples[move]/(move_samples[move]+1) + value / (move_samples[move] + 1)
                move_samples[move] += 1
            else:
                move_ratings[move] = value   
            i+=1

        self.engine.moves = moves_copy
        return move_ratings.index(max(move_ratings))


    #repeatedly choose random move until win or loss
    def sample(self, move):
        store_board = self.engine.board
        store_visible = self.engine.visible
        store_owner = self.engine.owner

        self.engine.board = self.engine.board.copy()
        self.engine.visible = self.engine.visible.copy()
        self.engine.owner = self.engine.owner.copy()

        self.engine.move(move)

        turn = 1 - self.player
        winner = 0
        while True:
            self.engine.all_legal_moves(turn)

            winner = self.engine.check_winner(turn)
            if winner:
                break
            
            all_moves = self.engine.moves
            number_of_moves = all_moves[0]
            move = random.randrange(0, number_of_moves)

            self.engine.move(move)

            turn = 1 - turn

        self.engine.board = store_board
        self.engine.visible = store_visible
        self.engine.owner = store_owner
        if winner == self.player:
            return 3
        if winner == 3:
            return .5
        return 0