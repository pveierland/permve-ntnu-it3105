import enum
import random
import sys

from vi.games.twentyfortyeight import State
from vi.search.grid import Action

class NodeType(enum.Enum):
    player = 1
    chance = 2

def expectiminimax(turn, state, depth):
    if not depth:
        return heuristic(state),
    if turn is NodeType.player:
        return min((expectiminimax(NodeType.chance, state.copy().move(action), depth - 1)[0], action)
                   for action in Action)
    elif turn is NodeType.chance:
        available = state.available()
        num_available = len(available)

        alpha = 0

        for row, column in available:
            alpha = alpha + 1.0 / num_available * 0.9 * expectiminimax(
                NodeType.player,
                state.copy().set_value(row, column, 2),
                depth - 1)[0]

            alpha = alpha + 1.0 / num_available * 0.1 * expectiminimax(
                NodeType.player,
                state.copy().set_value(row, column, 4),
                depth - 1)[0]

        return alpha,

def heuristic(state):
    values = [0] * 17
    h = 0
    x = 0

    for column in range(4):
        for row in range(4):
            v = state.get_value(row, column)
            if v:
                x = x + 1
                values[v] = values[v] + 1
                if values[v] < 2:
                    h = h + State.convert_compact_value_to_number(v)
                else:
                    h = h - 0.5 * State.convert_compact_value_to_number(v)
    
    h = h / x

    #for column in range(4):
    #    for row in range(3):
    #        a = state.get_value(row, column)
    #        b = state.get_value(row + 1, column)
    #        
    #        if a == b:
    #            h = h + a

    #for row in range(4):
    #    for column in range(3):
    #        a = state.get_value(row, column)
    #        b = state.get_value(row, column + 1)

    #        if a == b:
    #            h = h + a

    return h
    #return max(state.get_value(row, column)
    #           for column in range(4)
    #           for row in range(4))
