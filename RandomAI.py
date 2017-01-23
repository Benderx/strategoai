#currently just randomly selects a move
#next up: rate moves based on tree
import random

class RandomAI:
    def __init__(self, player, engine, *args):
        self.engine = engine
        self.player = player
        self.board = engine.get_board()
    

    def get_move(self, all_moves):
        c = random.choice(all_moves)
        return c