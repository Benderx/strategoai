import Renderer as r
import GameEngine as g
import time


class Human:
    def __init__(self, s, g = False, r = None):
        self.side = s
        self.gui = g
        self.renderer = r


    def get_move(self):
        # Implement console only functionality, need parser from command line.
        if self.gui == False:
            pass
        else:
            while True:
                p = self.renderer.get_mouse_square()
                if p.x < 0 or p.x > 9 or p.y < 0 or p.y > 9
                    print('Point selected is out of bounds, select again.')
                    continue

                moves = engine.legal_moves_for_piece(self, p, player):

                if len(moves) == 0:
                    print('You cant move that')
                    continue

                # populate arr with tuples of posible moves of the piece
                arr = []
                renderer.disp_pos_moves(arr)

                p = self.renderer.get_mouse_square()
                if p.x < 0 or p.x > 9 or p.y < 0 or p.y > 9
                    print('Point selected is out of bounds, select again.')
                    renderer.del_pos_moves(arr)
                    continue


# humans = 0, 1, 2
def play_game(engine, humans = 1, gui = False, renderer = None):
    players = []
    if humans == 0:
        players.append(YOURAIHERE(0, ARGS))
        players.append(YOURAIHERE(1, ARGS))
    elif humans == 1:
        players.append(Human(0, gui, renderer))
        players.append(YOURAIHERE(1, ARGS))
    elif humans == 2:
        players.append(Human(0, gui, renderer))
        players.append(Human(1, gui, renderer))
    else:
        raise Exception('This is a two player game, you listed more than 2 humans, or less than 0.')

    engine.board_setup()
    renderer.draw_board()

    playing = True
    turn = 0
    while playing:
        coord1, coord2 = players[turn].get_move()
        l, msg = engine.check_legal(coord1, coord2)
        if l == True:
            engine.move(coord1, coord2)
        else:
            print("Illegal move, move again please.")
            print(msg)
            continue

        if gui:
            renderer.refresh_board()
        engine.print_board()
        turn = 1 - turn


def main():
    engine = g.GameEngine()
    re = r.Renderer(engine.get_board())
    re.window_setup(500, 500)

    play_game(engine, 2, True, re)


main()

# time.sleep(2)

# l = engine.check_legal([0, 6], [0, 5], 1)
# if l == True:
#     engine.move([0, 6], [0, 5])
#     engine.print_board()
# else:
#     print(l[1])

# r.refresh_board()


# # http://stackoverflow.com/questions/20340018/while-loop-is-taking-forever-and-freezing-screen
# while True:
#   time.sleep(.1)
