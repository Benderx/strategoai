import math
import random
import graphics

class Renderer:

    def __init__(self):
        pass


    def draw_board(self, board):
        pass


    # Takes in width and height and sets up the Graphical Window.
    def window_setup(self, width, height):
        if __name__ == '__main__':
            win = graphics.GraphWin("Chess", width, height)
        else:
            return "Not the main thread/proccess!"
