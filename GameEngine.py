import math
import random
import inspect

class Piece:
	# 0: Flag
	# 1-7: normal 1 movers
	# 8: normal mover, kills bombs
	# 9: super mover
	# 10: bombs, no movement
	# 11: Spy

	def __init__(self, p, v = None, n = None):
		self.player = p
		self.value = v
		self.name = n
		self.visible = False


	# returns how many spaces the piece may move.
	def get_movement(self):
		if self.value > 0 and self.value < 9 or self.value == 11:
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
		self.board = [[0 for x in range(0, 10)] for y in range(0, 10)]


	def board_setup(self):
		for x in range(len(self.board)):
			for y in range(len(self.board)):
				self.board[x][y] = 0

		# Rivers
		self.board[2][4] = -1
		self.board[2][5] = -1
		self.board[3][4] = -1
		self.board[3][5] = -1

		self.board[6][4] = -1
		self.board[6][5] = -1
		self.board[7][4] = -1
		self.board[7][5] = -1

		for i in range(0, 2):
			starting_pieces = [[0, 'Flag', 1], [10, 'Bomb', 6], [11, 'Spy', 1], [9, 'Scout', 8], [9, 'Miner', 5], [7, 'Sergeant', 4], [6, 'Lieutenent', 4], [5, 'Captain', 4], [4, 'Major', 3], [3, 'Colonel', 2], [2, 'General', 1], [1, 'Marshall', 1]]
			starting_locations = []
			for x in range(0, 10):
				for y in range(0 + i*6, 4 + i*6):
					starting_locations.append((x, y, i))

			while len(starting_pieces) != 0:
				r1 = int(random.random()*(len(starting_pieces)))
				r2 = int(random.random()*(len(starting_locations)))

				p = Piece(starting_locations[r2][2], starting_pieces[r1][0])
				
				self.board[starting_locations[r2][0]][starting_locations[r2][1]] = p



				starting_locations.pop(r2)
				starting_pieces[r1][2] -= 1
				if starting_pieces[r1][2] == 0:
					starting_pieces.pop(r1)

	def print_board(self):
		for x in range(0, 10):
			arr_temp = []
			for y in range(0, 10):
				if isinstance(self.board[y][x], Piece):
					arr_temp.append(self.board[y][x].get_value())
				else:
					arr_temp.append(self.board[y][x])
			print(arr_temp)


	# Probably move this to a GameRenderer.py class
	def window_setup(self):
		if __name__ == '__main__':
			win = GraphWin("Chess", width, height)
		else:
			return "Not the main thread/proccess!"


p = GameEngine()
p.board_setup()
p.print_board()