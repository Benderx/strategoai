class Piece:
	# 0: Flag
	# 1-7: normal 1 movers
	# 8: normal mover, kills bombs
	# 9: super mover
	# 10: bombs, no movement

	def __init__(self, v = None, n = None):
		self.value = v
		self.name = n


	# returns [North, East, South, West] and how many spaces that piece may move.
	def get_movement():
		if self.value > 0 and self.value < 9
			return [1, 1, 1, 1]

		elif self.value == 0 or self.value == 10:
			return [0, 0, 0, 0]

		elif self.value == 9:
			return [30, 30, 30, 30]

		else:
			return "Piece value not found"


class GameEngine:
	def __init__(self):
		pass


	# Probably move this to a GameRenderer.py class
	def window_setup(self):
		if __name__ == '__main__':
    		win = GraphWin("Chess", width, height)
    	else:
    		return "Not the main thread/proccess!"