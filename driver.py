import Renderer as r
import GameEngine as g
import Human as h
import time
import sqlite3
import os


# humans = 0, 1, 2
def play_game(engine, humans = 1, db_stuff = None, gui = False, renderer = None):
    tracking = True
    if db_stuff == None:
        tracking = False

    players = []
    if humans == 0:
        players.append(YOURAIHERE(0, ARGS))
        players.append(YOURAIHERE(1, ARGS))
    elif humans == 1:
        players.append(h.Human(engine, 0, gui, renderer))
        players.append(YOURAIHERE(1, ARGS))
    elif humans == 2:
        players.append(h.Human(engine, 0, gui, renderer))
        players.append(h.Human(engine, 1, gui, renderer))
    else:
        raise Exception('This is a two player game, you listed more than 2 humans, or less than 0.')


    engine.board_setup()
    if gui:
        renderer.draw_board()
    else:
        engine.print_board()

    state_tracker = []
    state_tracker.append(engine.get_board_state())

    turn = 0
    while True:
        game_over, winner = engine.check_winner(turn)
        if game_over:
            break

        # We assume all player classes return valid moves.
        coord1, coord2 = players[turn].get_move()
        engine.move(coord1, coord2)

        # l, msg = engine.check_legal(coord1, coord2, turn)
        # if l == True:
        #     engine.move(coord1, coord2)
        # else:
        #     print('Illegal move, move again please.')
        #     print(msg)
        #     continue

        if gui:
            renderer.refresh_board()
        else:
            engine.print_board()

        turn = 1 - turn

    if tracking:
        sql_game_insert =   """
                                INSERT INTO Game (WINNER)
                                VALUES (%s);
                            """
        db_stuff[1].execute(sql_game_insert, str(winner))

        game_id = db_stuff[1].lastrowid
        state_tracker_packed = []
        for i in state_tracker:
            state_tracker_packed.append((str(game_id), str(i)))

        sql_state_insert =  """
                                INSERT INTO State (GAME_ID, BOARD)
                                VALUES (%s, %s);
                            """
        db_stuff[1].executemany(sql_state_insert, state_tracker_packed)

        db_stuff[0].commit()


# Takes in database name and if you want to overwrite current, or add to it. Probably change in future for streamlined data creation
# Returns sqlite3 db connection
def init_db(dbpath = 'test.db', overwrite = True):
    exist = False
    if os.path.isfile(dbpath):
        exist = True

    if overwrite and exist:
        os.remove(dbpath)
    
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    if overwrite or exist == False:
        sql_create_game =   """
                                CREATE TABLE Game (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                WINNER INTEGER NOT NULL);
                            """
        cursor.execute(sql_create_game)

        # How should we store the board?
        sql_create_state =  """
                                CREATE TABLE State (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                GAME_ID INTEGER NOT NULL,
                                BOARD CHAR(500) NOT NULL,
                                FOREIGN KEY (GAME_ID) REFERENCES Game(ID));
                            """
        cursor.execute(sql_create_state)
    return [conn, cursor]


def main():
    engine = g.GameEngine()
    re = r.Renderer(engine.get_board())
    re.window_setup(500, 500)

    db_stuff = init_db('games.db', True)
    play_game(engine, 2, db_stuff, True, re)
    db_stuff[0].close()
main()







# time.sleep(2)

# l = engine.check_legal([0, 6], [0, 5], 1)
# if l == True:
#     engine.move([0, 6], [0, 5])
#     engine.print_board()
# else:
#     print(l[1])

# r.refresh_board()


# # http://stackoverflow.com/questions/20340018/while-loop-is-taking-forever-and-freezing-screen
# while True:
#   time.sleep(.1)
