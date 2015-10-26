#!/usr/bin/python
import enum
import random
import sys
import numpy
import time

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

from vi.games.twentyfortyeight import *
from vi.search.grid import Action

class Game(object):

    def __init__(self):
        self.transposition_table = {}
        self.max_depth       = 0
        self.moves_evaluated = 0
        self.cache_hits      = 0

    def move_player(self):
        pass

    def find_move(self, board):
        return max((self.score_move(board, action), action) for action in Action)[1]

    def score_move(self, board, action):
        new_board = board.move(action)
        if new_board == board:
            return 0
        return self.score_tilespawn_node(new_board, 0, 1.0) + 0.000001

    def score_move_node(self, board, depth, probability):
        score = 0

        for action in range(4):
            new_board = board.move(action)
            self.moves_evaluated += 1
            if board != new_board:
                score = max(score,
                            self.score_tilespawn_node(new_board, depth + 1, probability))

        return score

    def score_tilespawn_node(self, board, depth, probability):
        if probability < 0.0001 or depth >= 3:
            self.max_depth = max(self.max_depth, depth)
            return board.heuristic()

        transposition_lookup = self.transposition_table.get(board)

        if transposition_lookup:
            transposition_depth, transposition_score = transposition_lookup
            if transposition_depth <= depth:
                self.cache_hits += 1
                return transposition_score

        score = 0.0
        available = board.available()

        if available:
            num_available  = float(len(available))
            probability   /= num_available

            for row, column in available:
                score += 0.9 * self.score_move_node(board.spawn(row, column, 2),
                                                    depth, probability)
                score += 0.1 * self.score_move_node(board.spawn(row, column, 4),
                                                    depth, probability)

            score /= num_available
            self.transposition_table[board] = (depth, score)

        return score
#
#SCORE_LOST_PENALTY = 200000.0
#SCORE_MONOTONICITY_POWER = 4.0
#SCORE_MONOTONICITY_WEIGHT = 47.0
#SCORE_SUM_POWER = 3.5
#SCORE_SUM_WEIGHT = 11.0
#SCORE_MERGES_WEIGHT = 700.0
#SCORE_EMPTY_WEIGHT = 270.0
#
#def heuristic(state):
#
#    total_score = 0
#
#    for column in range(4):
#        score   = 0
#        empty   = 0
#        merges  = 0
#
#        prev    = 0
#        counter = 0
#
#        for row in range(4):
#            rank = state.get_value(row, column)
#            score += pow(rank, SCORE_SUM_POWER)
#
#            if not rank:
#                empty += 1
#            else:
#                if prev == rank:
#                    counter += 1
#                elif counter > 0:
#                    merges += 1 + counter
#                    counter = 0
#                prev = rank
#
#        if counter > 0:
#            merges += 1 + counter
#
#        mleft = 0
#        mright = 0
#
#        for row in range(1,4):
#            if state.get_value(row - 1, column) > state.get_value(row, column):
#                mleft += pow(state.get_value(row - 1, column), SCORE_MONOTONICITY_POWER) - \
#                         pow(state.get_value(row, column), SCORE_MONOTONICITY_POWER)
#            else:
#                mright += pow(state.get_value(row, column), SCORE_MONOTONICITY_POWER) - \
#                          pow(state.get_value(row - 1, column), SCORE_MONOTONICITY_POWER)
#
#        total_score += SCORE_LOST_PENALTY + \
#            SCORE_EMPTY_WEIGHT * empty + \
#            SCORE_MERGES_WEIGHT * merges - \
#            SCORE_MONOTONICITY_WEIGHT * min(mleft, mright) - \
#            SCORE_SUM_WEIGHT * score
#
#    for row in range(4):
#        score   = 0
#        empty   = 0
#        merges  = 0
#
#        prev    = 0
#        counter = 0
#
#        for column in range(4):
#            rank = state.get_value(row, column)
#            score += pow(rank, SCORE_SUM_POWER)
#
#            if not rank:
#                empty += 1
#            else:
#                if prev == rank:
#                    counter += 1
#                elif counter > 0:
#                    merges += 1 + counter
#                    counter = 0
#                prev = rank
#
#        if counter > 0:
#            merges += 1 + counter
#
#        mleft = 0
#        mright = 0
#
#        for column in range(1,4):
#            if state.get_value(row, column - 1) > state.get_value(row, column):
#                mleft += pow(state.get_value(row, column - 1), SCORE_MONOTONICITY_POWER) - \
#                         pow(state.get_value(row, column), SCORE_MONOTONICITY_POWER)
#            else:
#                mright += pow(state.get_value(row, column), SCORE_MONOTONICITY_POWER) - \
#                          pow(state.get_value(row, column - 1), SCORE_MONOTONICITY_POWER)
#
#        total_score += SCORE_LOST_PENALTY + \
#            SCORE_EMPTY_WEIGHT * empty + \
#            SCORE_MERGES_WEIGHT * merges - \
#            SCORE_MONOTONICITY_WEIGHT * min(mleft, mright) - \
#            SCORE_SUM_WEIGHT * score
#
#    return total_score

def game():
    def populate(state):
        available = state.available()
        if available:
            state.set_value(*random.choice(state.available()),
                            value=2 if random.random() < 0.9 else 4)
            return True
        else:
            return False

    game  = Game()
    board = Board()

    time_start = time.time()

    #with PyCallGraph(output=GraphvizOutput()):
    #while True:
    if not populate(board):
        print("GAME OVER! HIGHEST TILE = {0}".format(
              board.get_highest_value()))
        sys.exit(-1)

    move  = game.find_move(board)
    board = board.move(move)

    print('{0}\n'.format(board))

    time_stop = time.time()

    print("Time elapsed = {0}. Moves evaluated = {1}. Cache hits = {2}".format(
        time_stop - time_start, game.moves_evaluated, game.cache_hits))

if __name__ == '__main__':
    game()
