import Renderer as r
import GameEngine as g
import time



engine = g.GameEngine()
r = r.Renderer(engine.get_board())
r.window_setup(500, 500)
r.draw_board()


while True:
	time.sleep(1)

engine.board_setup()

engine.print_board()

l = engine.check_legal([0, 6], [0, 5], 1)
if l == True:
    engine.move([0, 6], [0, 5])
    engine.print_board()
else:
    print(l)



