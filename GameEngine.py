import math

class Piece:
	# 0: Flag
	# 1-7: normal 1 movers
	# 8: normal mover, kills bombs
	# 9: super mover
	# 10: bombs, no movement

	def __init__(self, v = None, n = None):
		self.value = v
		self.name = n
		self.visible = False


	# returns how many spaces the piece may move.
	def get_movement(self):
		if self.value > 0 and self.value < 9:
			return 1

		elif self.value == 0 or self.value == 10:
			return 0

		elif self.value == 9:
			return math.inf

		else:
			return "Piece value not found"


	def get_visibility(self):
		return self.visible


	def get_value(self):
		return self.value


	def get_name(self):
		return self.name


class GameEngine:
	def __init__(self):
		pass


	# Probably move this to a GameRenderer.py class
	def window_setup(self):
		if __name__ == '__main__':
			win = GraphWin("Chess", width, height)
		else:
			return "Not the main thread/proccess!"


p = Piece(9)
print(p.get_movement())