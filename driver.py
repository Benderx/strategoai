
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

GAMES_FILEPATH = 'games'


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



def play_back_game(engine, results, renderer, board_size, track, monte_samples, game_id):
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
    def flatten_xy(x, y):
        return x + y * (board_size)


    turn = 0
    moves_this_game = results[1]
    board_arr, visible_arr, owner_arr, movement_arr, move_from_arr, move_to_arr, move_from_arr_one_hot, move_to_arr_one_hot, move_data, taken_rating, taken_samples = [], [], [], [], [], [], [], [], [], [], []
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

        if track == 1 and turn == 1:
            move_from = flatten_xy(tot_move[0], tot_move[1])
            move_to = flatten_xy(tot_move[2], tot_move[3])

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
                for k in monte_moves:
                    if k[0] == (tot_move[0], tot_move[1], tot_move[2], tot_move[3]):
                        # print(k)
                        taken_rating.append(k[1])
                        taken_samples.append(k[2])
                        break



        engine.move(tot_move)

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
                           'move_data': move_data, 'board_size': board_size, 'samples': monte_samples, 'game_id': game_id,
                           'move_rating': taken_rating, 'move_samples': taken_samples})
        if os.path.isfile("games"):
            old = pandas.read_pickle("games")
            df = pandas.concat([old, df], ignore_index=True, axis=0)
            # os.remove("games")

        df.to_pickle("games")
        print('Tracking game_id', game_id)



# def play_c_game(engine, AI1 = None, AI2 = None, board_size = 10, monte_samples = 1):
#     start = time.perf_counter()
#     results = c_bindings.game_wrapper(0, 1, monte_samples, board_size, 2)
#     end = time.perf_counter()

#     tot_time = start-end
#     return (results, tot_time)


def play_c_games(AI1 = None, AI2 = None, board_size = 10, monte_samples = 1):
    start = time.perf_counter()
    results = c_bindings.game_wrapper(0, 1, monte_samples, board_size, 8)
    end = time.perf_counter()

    tot_time = end-start
    return (results, tot_time)


def game_start(args):
    engine = g.GameEngine(int(args.size))
    re = None
    num_games = int(args.number)
    monte_samples = int()

    game_id = 0
    if os.path.isfile("games"):
        old = [pandas.read_pickle("games")]
        game_id = old[0]['game_id'].iloc[-1] + 1
        del old  #frees memory

    print('Starting tracking from:', game_id)

    i = 0
    while i < num_games:
        result_tuple = play_c_games(FIRST_AI, SECOND_AI, int(args.size), monte_samples)
        results = result_tuple[0]
        timer = result_tuple[1]

        print('game_ends:', results[0:8])
        start_point = 8

        for p in range(0, 8):
            print('game', (int(i/8)*8)+p, ': ', results[int(start_point)], ' won in', results[int(start_point+1)], 'moves', 'MP_PC:', (timer/8.0))

            # if int(args.graphical) == 1 or int(args.track) == 1:
            #     if int(args.graphical) == 1:
            #         re = r.Renderer(engine)
            #         re.window_setup(500, 500)

            #     play_back_game(engine, results, re, int(args.size), int(args.track), monte_samples, game_id + i)

            start_point = results[p]
            i += 1



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graphical', default=1, help='whether or not to show the gui')
    parser.add_argument('--number', default=1, help='How many games to play')
    parser.add_argument('--size', default=6, help='How big the board is')
    parser.add_argument('--track', default=0, help='If game tracking happens')
    parser.add_argument('--samples', default=1000, help='How many times to sample per move')
    args = parser.parse_args()

    game_start(args)

    
if __name__ == '__main__':
    main()
