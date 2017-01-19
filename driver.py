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
				p = self.renderer.get_mouse()
				# Program in mouse getting


# humans = 0, 1, 2
def play_game(humans = 1, gui = False, renderer = None):
	players = []
	if humans == 0:
		players.append(Human(0, gui, renderer))
	elif humans == 1:

	elif humans == 2:
		players.append(Human(0))
	else:
		raise Exception('This is a two player game, you listed more than 2 humans, or less than 0.')

	playing = True
	turn = 0
	while playing:
		players[turn].get_move()


		turn = 1 - turn


def main():
	engine = g.GameEngine()
	r = r.Renderer(engine.get_board())
	r.window_setup(500, 500)

	engine.board_setup()
	r.draw_board()


	play_game(2, True, r)


main()

# time.sleep(2)

# l = engine.check_legal([0, 6], [0, 5], 1)
# if l == True:
#     engine.move([0, 6], [0, 5])
#     engine.print_board()
# else:
#     print(l)

# r.refresh_board()


# # http://stackoverflow.com/questions/20340018/while-loop-is-taking-forever-and-freezing-screen
# while True:
# 	time.sleep(.1)
