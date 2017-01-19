#currently just randomly selects a move
#next up: rate moves based on tree
import random

class GaussianAI:
    def __init__(self, engine):
        self.engine = engine
    def get_move(self, board, player):
        all_moves = self.engine.all_legal_moves(player)
        print(all_moves)
        return random.choice(all_moves)