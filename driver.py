import Renderer as r
import GameEngine as g


r = r.Renderer()
r.window_setup(500, 500)


p = g.GameEngine()
p.board_setup()

p.print_board()

l = p.check_legal([0, 6], [0, 5], 1)
if l == True:
    p.move([0, 6], [0, 5])
    p.print_board()
else:
    print(l)
