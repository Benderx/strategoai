import random
import GameEngine
from copy import deepcopy
import RandomAI
import time

TOTAL_SAMPLES = 10

class MonteCarloAI:
    def __init__(self, player, engine, depth = 1):
        self.engine = engine
        self.player = player
        self.board = engine.get_board()
        self.trans_table = {} # tbd
    

    def get_move(self, all_moves):
        
        i = 0
        move_ratings = [-1 for x in range(len(all_moves))]
        move_samples = [1 for x in range(len(all_moves))]

        while i < TOTAL_SAMPLES:
            loc = i%len(all_moves)

            s = time.time()
            value = self.sample(all_moves[loc])
            e = time.time()
            print('total' + str(e-s))

            if move_ratings[loc] != -1:
                move_ratings[loc] = move_ratings[loc]*move_samples[loc]/(move_samples[loc]+1) + value / (move_samples[loc] + 1)
                move_samples[loc] += 1
            else:
                move_ratings[loc] = value   
            i+=1
        # print('lol')
        print(move_ratings)
        return all_moves[move_ratings.index(max(move_ratings))]


    #repeatedly choose random move until win or loss
    def sample(self, move):
        parent_board = deepcopy(self.engine.board)

        self.engine.board = parent_board

        self.engine.move(move[0], move[1])
        turn = 1 - self.player
        winner = None
        while True:
            
            moves = self.engine.all_legal_moves(turn)

            game_over, winner = self.engine.check_winner(turn, moves)
            if game_over:
                break
            
            move = random.choice(moves)
            self.engine.move(move[0], move[1])

            turn = 1 - turn

        self.engine.board = self.board
        if winner == self.player:
            return 1
        if winner == 2:
            return .5
        return 0