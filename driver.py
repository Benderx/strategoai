import Renderer as r
import GameEngine as g
import time
import sqlite3
import os


# humans = 0, 1, 2
def play_game(engine, humans = 1, db_conn = None, gui = False, renderer = None):
    tracking = True
    if db_conn == None:
        tracking = False

    players = []
    if humans == 0:
        players.append(YOURAIHERE(0, ARGS))
        players.append(YOURAIHERE(1, ARGS))
    elif humans == 1:
        players.append(Human(engine, 0, gui, renderer))
        players.append(YOURAIHERE(1, ARGS))
    elif humans == 2:
        players.append(Human(engine, 0, gui, renderer))
        players.append(Human(engine, 1, gui, renderer))
    else:
        raise Exception('This is a two player game, you listed more than 2 humans, or less than 0.')


    engine.board_setup()
    if gui:
        renderer.draw_board()
    else:
        engine.print_board()

    if tracking:
        pass
        # record_board(engine)

    playing = True
    turn = 0
    while playing:
        coord1, coord2 = players[turn].get_move()

        # This checking doesnt need to happen probably
        l, msg = engine.check_legal(coord1, coord2, turn)
        if l == True:
            engine.move(coord1, coord2)
        else:
            print('Illegal move, move again please.')
            print(msg)
            continue

        if gui:
            renderer.refresh_board()
        else:
            engine.print_board()
        turn = 1 - turn


# Takes in database name and if you want to overwrite current, or add to it. Probably change in future for streamlined data creation
# Returns sqlite3 db connection
def init_db(dbname = 'test.db', overwrite = True):
    exist = False
    if os.fileexists(dbpath)
        exist = True

    if overwrite and exist:
        os.remove(dbpath)
    
    conn = sqlite3.connect(dbpath)

    if overwrite or exist == False:
        create_game_sql = """
                        CREATE TABLE Game (
                       ID INT PRIMARY KEY AUTOINCREMENT,
                       WINNER INT);
                    """
        conn.execute(create_game_sql)

        # How should we store the board?
        create_state_sql = """
                        CREATE TABLE State (
                       ID INT PRIMARY KEY AUTOINCREMENT,
                       GAME_ID INT FOREIGN KEY NOT NULL,
                       BOARD CHAR(500) NOT NULL);
                    """
        conn.execute(create_state_sql)
    return conn


def main():
    engine = g.GameEngine()
    re = r.Renderer(engine.get_board())
    re.window_setup(500, 500)

    db_conn = init_db('games.db', True)
    play_game(engine, 2, db_conn, True, re)

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
