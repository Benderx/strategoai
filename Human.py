class Human:
    def __init__(self, engine, side, gui = False, renderer = None):
        self.side = side
        self.gui = gui
        self.renderer = renderer
        self.engine = engine


    def get_move(self):
        # Implement console only functionality, need parser from command line.
        if self.gui == False:
            pass
        else:
            while True:
                coord1 = self.renderer.get_mouse_square()
                if coord1[0] < 0 or coord1[0] > 9 or coord1[1] < 0 or coord1[1] > 9:
                    print('Point selected is out of bounds, select again.')
                    continue

                moves = self.engine.legal_moves_for_piece(coord1, self.side)


                if len(moves) == 0:
                    print('You cant move that')
                    continue

                # populate arr with tuples of posible moves of the piece
                self.renderer.disp_pos_moves(moves)

                coord2 = self.renderer.get_mouse_square()
                if coord2[0] < 0 or coord2[0] > 9 or coord2[1] < 0 or coord2[1] > 9:
                    print('Point selected is out of bounds, select again.')
                    self.renderer.del_disp_moves()
                    continue

                self.renderer.del_disp_moves()
                given_move = (coord1, coord2)
                if given_move in moves:
                    return given_move[0], given_move[1]