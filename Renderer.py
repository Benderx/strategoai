import math
import random
import graphics

class Renderer:

    def __init__(self, b, l = 15):
        self.board = b
        self.box_length = l
        piece_arr = []
        self.win = None


    def draw_board(self):
        for i in range(len(self.board_):
            for j in range(len(self.board[i])):
                piece = Text(Point(self.box_length * i + offset + (self.box_ength / 2),
                                      self.box_length * j + offset + (self.box_length / 2)), "NO")
                piece_arr.append(piece)
                piece.draw(win)


    # Takes in width and height and sets up the Graphical Window.
    def window_setup(self, width, height):
        if __name__ == '__main__':
            self.win = graphics.GraphWin("Chess", width, height)
        else:
            return "Not the main thread/proccess!"
