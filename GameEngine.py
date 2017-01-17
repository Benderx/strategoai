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


	def get_player(self):
		return self.player


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


	# Takes in coord1 [x1, y1] and coord2 [x2, y2], and player = (0 or 1)
	def check_legal(self, coord1, coord2, player)
		if coord1[0] < 0  or coord1[0] > 9:
			return "coord1 x is out of bounds"
		if coord1[1] < 0  or coord1[1] > 9:
			return "coord1 y is out of bounds"
		if coord2[0] < 0  or coord2[0] > 9:
			return "coord2 x is out of bounds"
		if coord2[1] < 0  or coord2[1] > 9:
			return "coord2 y is out of bounds"

		if coord1[0] == 2 and coord1 == 4:
			return "you cant move the lake silly."
		if coord1[0] == 2 and coord1 == 5:
			return "you cant move the lake silly."
		if coord1[0] == 3 and coord1 == 4:
			return "you cant move the lake silly."
		if coord1[0] == 3 and coord1 == 5:
			return "you cant move the lake silly."

		if coord1[0] == 6 and coord1 == 4:
			return "you cant move the lake silly."
		if coord1[0] == 6 and coord1 == 5:
			return "you cant move the lake silly."
		if coord1[0] == 7 and coord1 == 4:
			return "you cant move the lake silly."
		if coord1[0] == 7 and coord1 == 5:
			return "you cant move the lake silly."

		if coord2[0] == 2 and coord2 == 4:
			return "you cant move the lake silly."
		if coord2[0] == 2 and coord2 == 5:
			return "you cant move the lake silly."
		if coord2[0] == 3 and coord2 == 4:
			return "you cant move the lake silly."
		if coord2[0] == 3 and coord2 == 5:
			return "you cant move the lake silly."

		if coord2[0] == 6 and coord2 == 4:
			return "you cant move the lake silly."
		if coord2[0] == 6 and coord2 == 5:
			return "you cant move the lake silly."
		if coord2[0] == 7 and coord2 == 4:
			return "you cant move the lake silly."
		if coord2[0] == 7 and coord2 == 5:
			return "you cant move the lake silly."


		if not isinstance(self.board[coord1[0]][coord1[1]], Piece):
			return "coord1 is invalid, there is no piece there"
		piece = self.board[coord1[0]][coord1[1]]
		if piece.get_player() != player:
			return "That is not your piece"

		xdist = math.abs(coord1[0] - coord2[0])
		ydist = math.abs(coord1[1] - coord2[1])

		if xdist != 0 and ydist != 0:
			return "you cannot move diagonally"

		move = piece.get_movement()
		if xdist > move: or ydist > move:
			return "the piece you are moving cannot move like that"

		piece2 = self.board[coord2[0]][coord2[1]]
		if piece.get_player() == piece2.get_player():
			return "You cant move into your own piece"

		return True


	# Takes in 2 players and returns 0 for p1 winning and 1 for p2 winning.
	# Something about revealing here.
	def battle(self, p1, p2):



	# Takes in coord1 [x1, y1] and coord2 [x2, y2], and player = (0 or 1)
	# This assumes check_legal has been run.
	def move(self, coord1, coord2):
		p1 = self.board[coord1[0]][coord1[1]]
		if not isinstance(self.board[coord2[0]][coord2[1]], Piece):
			self.board[coord2[0]][coord2[1]] = p1
			self.board[coord1[0]][coord1[1]] = 0
			return True

		p2 = self.board[coord2[0]][coord2[1]]
		winner = self.battle(p1, p2)
		if winner == 0:
			self.board[coord2[0]][coord2[1]] = p1

		# Something about revealing here.
		return True



	# Probably move this to a GameRenderer.py class
	def window_setup(self):
		if __name__ == '__main__':
			win = GraphWin("Chess", width, height)
		else:
			return "Not the main thread/proccess!"


p = GameEngine()
p.board_setup()
p.print_board()