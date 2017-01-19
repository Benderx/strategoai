import GameEngine as g
import Renderer as r
import GaussianAI as gauss


engine = g.GameEngine()
engine.board_setup()
r = r.Renderer(engine.get_board())
r.window_setup(500, 500)
ai = gauss.GaussianAI(engine)

r.draw_board()


while True:
    move = ai.get_move(engine.get_board(), player = 1)
    print(move)
    input()
    engine.move(*move)
    r.refresh_board()
