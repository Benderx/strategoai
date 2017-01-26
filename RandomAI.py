#currently just randomly selects a move
#next up: rate moves based on tree
import random

class RandomAI:
    def __init__(self, player, engine, *args):
        self.engine = engine
        self.player = player
        self.type = 0
    

    def get_move(self):
        all_moves = self.engine.moves
        number_of_moves = all_moves[0]
        c = random.randrange(0, number_of_moves)
        return c