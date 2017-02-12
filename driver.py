
import Renderer as r
import GameEngine as g
import time
import sqlite3
import os
import argparse
import c_bindings.engine_commands as c_bindings
import pandas
import numpy
from copy import deepcopy


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
    def one_hot(val):
        temp = numpy.zeros(36, dtype = "float")
        temp[val] = 1
        return temp
    def fix_owner(list):
        temp = []
        for i in range(len(list)):
            if list[i] == 0:
                temp.append(1)
            elif list[i] == 1:
                temp.append(2)
            elif list[i] == 2:
                temp.append(0)
            else:
                raise ValueError("visibility array is broken")
        return numpy.asarray(temp, dtype = "float")
    def decode_xy(x, y):
        return [x + y * (board_size)]


    turn = 0
    moves_this_game = results[1]
    board_arr, visible_arr, owner_arr, movement_arr, move_from_arr, move_to_arr, move_from_arr_one_hot, move_to_arr_one_hot, move_data = [], [], [], [], [], [], [], [], []
    while True:
        if renderer != None:
            renderer.draw_board()
        move = results[counter:counter+6]


        done, tot_move, move_type, rating, sample = engine.examine_move(move)
        if done == None:
            break

        monte_moves = []
        # read monte move
        if move_type != 1:
            while True:
                monte_moves.append((tot_move, rating, sample))

                counter += 6
                move = results[counter:counter+6]
                done, tot_move, move_type, rating, sample = engine.examine_move(move)
                if done == None:
                    raise Exception("this should never happen")
                if move_type == 1:
                    break

        engine.move(tot_move)

        if track == 1 and turn == 1:
            move_from = decode_xy(tot_move[0], tot_move[1])
            move_to = decode_xy(tot_move[2], tot_move[3])

            board_arr.append(deepcopy(engine.board))
            visible_arr.append(deepcopy(engine.visible))
            owned = fix_owner(engine.owner)
            owner_arr.append(owned)
            movement_arr.append(deepcopy(engine.movement))

            move_from_arr_one_hot.append(one_hot(move_from))
            move_to_arr_one_hot.append(one_hot(move_to)) 

            move_from_arr.append(move_from)
            move_to_arr.append(move_to)

            if len(monte_moves) == 0:
                move_data.append(None)
            else:
                move_data.append(monte_moves)

        counter += 6
        turn = 1- turn
        if renderer != None:
            time.sleep(.5)
    if track == 1:
        # print(len(board_arr[0]))
        df = pandas.DataFrame.from_dict({'board':board_arr, 'visible': visible_arr,
                           'owner': owner_arr, 'movement': movement_arr,
                           'move_from': move_from_arr, 'move_to': move_to_arr,
                           'move_from_one_hot': move_from_arr_one_hot, 'move_to_one_hot': move_to_arr_one_hot,
                           'move_data': move_data, 'board_size': board_size})
        if os.path.isfile("games"):
            old = pandas.read_pickle("games")
            df = pandas.concat([df, old], ignore_index=True, axis=0)

        df.to_pickle("games")
        print('Tracking game', game_iter)



def play_c_game(engine, AI1 = None, AI2 = None, board_size = 10):
    start = time.perf_counter()
    results = c_bindings.play_game(0, 1, 5000, board_size)
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
