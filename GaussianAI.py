#currently just randomly selects a move
#next up: rate moves based on tree
import random

class GaussianAI:
    def __init__(self, player, engine):
        self.engine = engine
        self.player = player
    def get_move(self, board):
        all_moves = self.engine.all_legal_moves(self.player)
        print(all_moves)
        return random.choice(all_moves)