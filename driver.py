
import Renderer as r
import GameEngine as g
import time
import sqlite3
import os
import argparse
import c_bindings.engine_commands as c_bindings
import pandas


FIRST_AI = 0 #RANDOM
SECOND_AI = 1 #MONTE

GAMES_FILEPATH = 'games.csv'


def print_moves_per_second(thread_name, delay, c):
    global moves_per_second;
    count = 0
    last = time.perf_counter()
    while count < c:
        count += 1
        while not time.perf_counter() - last > 1:
            time.sleep(.05)
        last = time.perf_counter()
        print('Moves per perf: ' + str(moves_per_second))
        moves_per_second = 0



def play_back_game(engine, results, renderer, board_size, track, game_iter):
    counter = engine.board_setup(results, board_size)

    turn = 0
    moves_this_game = results[1]

    board, visible, owner, movement, moves_from, moves_to = [], [], [], [], [], []
    while True:
        if renderer != None:
            renderer.draw_board()

        move = results[counter:counter+4]
        move_from, move_to = engine.move(move, board_size)
        if move_from == None:
            break
        if track == 1:
            board.append(engine.board)
            visible.append(engine.visible)
            owner.append(engine.owner)
            movement.append(engine.movement)
            moves_from.append(move_from)
            moves_to.append(move_to)

        counter += 4
        turn = 1- turn
        if renderer != None:
            time.sleep(.5)
    if track == 1:
        # game_id = game_iter
        df = pandas.DataFrame({'board':board, 'visible': visible,
                           'owner': owner, 'movement': movement,
                           'move_from': moves_from, 'move_to': moves_to,
                           'board_size': board_size})
        if os.path.isfile("games"):
            old = pandas.read_pickle("games")
            df = pandas.concat([df, old], ignore_index=True, axis=0)

            print(df)
        df.to_pickle("games")
        # if not os.path.isfile('games.csv') or True:
        #     df.to_csv(GAMES_FILEPATH)
        # else:
        #     with open(GAMES_FILEPATH, 'a') as file:
        #         df.to_csv(file, header=False)
        print('Tracking game', game_iter)

    if renderer != None:
        input()
    input()



def play_c_game(engine, AI1 = None, AI2 = None, board_size = 10):
    start = time.perf_counter()
    results = c_bindings.play_game(0, 1, 50, board_size)
    end = time.perf_counter()

    return results, end-start


def game_start(args):
    engine = g.GameEngine(int(args.size))
    re = None
    num_games = int(args.number)


    for i in range(num_games):
        results, time = play_c_game(engine, FIRST_AI, SECOND_AI, int(args.size))
        print('game ', i, ': ', results[0], ' won in', results[1], 'moves', 'MP_PC:', float(results[1])/time)

        if int(args.graphical) == 1 or int(args.track) == 1:
            if int(args.graphical) == 1:
                re = r.Renderer(engine)
                re.window_setup(500, 500)

            play_back_game(engine, results, re, int(args.size), int(args.track), i)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('graphical', default=1, help='whether or not to show the gui')
    parser.add_argument('number', default=1, help='How many games to play')
    parser.add_argument('size', default=10, help='How big the board is')
    parser.add_argument('track', default=1, help='If database tracking happens')
    args = parser.parse_args()

    game_start(args)

    
if __name__ == '__main__':
    main()
