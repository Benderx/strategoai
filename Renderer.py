import math
import random
import graphics

class Renderer:

    def __init__(self, b, l = 40, o = 5):
        self.board = b
        self.box_length = l
        self.offset = o
        self.piece_arr = []
        self.win = None


    # Only for initial draw
    def draw_board(self):
        lakes = [(2,4), (2,5), (3,4), (3,5),
                (6,4), (6,5), (7,4), (7,5)]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i, j) in lakes:
                    continue

                c = graphics.Rectangle(graphics.Point(self.box_length * i + self.offset, self.box_length * j + self.offset),
                          graphics.Point(self.box_length * (i+1) + self.offset, self.box_length * (j+1) + self.offset))
                c.draw(self.win)

                if type(0) == type(self.board[i][j]):
                    continue

                piece = graphics.Text(graphics.Point(self.box_length * i + self.offset + (self.box_length / 2),
                                      self.box_length * j + self.offset + (self.box_length / 2)), "NO")
                if self.board[i][j].get_value() == 0:
                    piece.setText('F')
                elif self.board[i][j].get_value() == 10:
                    piece.setText('B')
                elif self.board[i][j].get_value() == 11:
                    piece.setText('S')
                else:
                    piece.setText(str(self.board[i][j].get_value()))


                self.piece_arr.append(piece)
                piece.draw(self.win)


    # Used for refreshing to save space and time.
    def refresh_board(self):
        for i in self.piece_arr:
            i.undraw()
        self.piece_arr = []

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if type(0) == type(self.board[i][j]):
                    continue

                piece = graphics.Text(graphics.Point(self.box_length * i + self.offset + (self.box_length / 2),
                                      self.box_length * j + self.offset + (self.box_length / 2)), "NO")
                if self.board[i][j].get_value() == 0:
                    piece.setText('F')
                elif self.board[i][j].get_value() == 10:
                    piece.setText('B')
                elif self.board[i][j].get_value() == 11:
                    piece.setText('S')
                else:
                    piece.setText(str(self.board[i][j].get_value()))


                self.piece_arr.append(piece)
                piece.draw(self.win)
    

    def get_mouse_square(self):
        p = self.win.getMouse()
        width = int(p.x / self.box_length)
        height = int(p.y / self.box_length)
        return (width, height)


    # takes in array of tuples and highlights those on the board.
    def disp_pos_moves(self, arr)
        pass


    # Takes in width and height and sets up the Graphical Window.
    def window_setup(self, width, height):
        if __name__ == 'Renderer':
            self.win = graphics.GraphWin("Stratego!", width, height)
            self.win.setBackground("tan2")
        else:
            print("Not the main thread/proccess!")
            return 
