import Renderer as r
import GameEngine as g
import time



engine = g.GameEngine()
r = r.Renderer(engine.get_board())
r.window_setup(500, 500)

engine.board_setup()
r.draw_board()


time.sleep(2)

l = engine.check_legal([0, 6], [0, 5], 1)
if l == True:
    engine.move([0, 6], [0, 5])
    engine.print_board()
else:
    print(l)

r.refresh_board()


# http://stackoverflow.com/questions/20340018/while-loop-is-taking-forever-and-freezing-screen
while True:
	time.sleep(.1)
