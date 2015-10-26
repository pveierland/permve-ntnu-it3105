import math
import numpy

from vi.search.grid import Action

def _initialize_heuristic_lookup_table():
    heuristic_lookup_table = numpy.zeros(
        numpy.iinfo(numpy.uint16).max + 1, dtype=float)

    SCORE_LOST_PENALTY = 200000.0
    SCORE_MONOTONICITY_POWER = 4.0
    SCORE_MONOTONICITY_WEIGHT = 47.0
    SCORE_SUM_POWER = 3.5
    SCORE_SUM_WEIGHT = 11.0
    SCORE_MERGES_WEIGHT = 700.0
    SCORE_EMPTY_WEIGHT = 270.0

    for row in range(numpy.iinfo(numpy.uint16).max + 1):
        empty = 0
        for i in range(4):
            empty += ((row >> (4 * i)) & 0b1111) == 0

        heuristic_lookup_table[row] = \
            SCORE_LOST_PENALTY + SCORE_EMPTY_WEIGHT * empty

    return heuristic_lookup_table

def _initialize_move_lookup_table():
    def reverse_row(row):
        return ((row & 0xF000) >> 12) | ((row & 0x0F00) >> 4) | \
               ((row & 0x000F) << 12) | ((row & 0x00F0) << 4)

    def unpack_column(row):
        return (row | (row << 12) | (row << 24) | (row << 36)) & 0x000F000F000F000F

    def pack_column(row):
        return ((row >> 36) & 0xF000) | \
               ((row >> 24) & 0x0F00) | \
               ((row >> 12) & 0x00F0) | \
               (row & 0xF)

    move_lookup_table = numpy.zeros(
        (4, numpy.iinfo(numpy.uint16).max + 1), dtype=int)

    for row in range(numpy.iinfo(numpy.uint16).max + 1):
        result        = 0
        output_offset = 0

        index = 0
        while index < 3:
            offset       = 4 * index
            current_cell = (row & (0b1111 << offset)) >> offset

            if current_cell:
                next_cell = (row & (0b1111 << (offset + 4))) >> (offset + 4)

                if current_cell == next_cell:
                    result |= (current_cell + 1) << output_offset
                    index  += 1
                else:
                    result |= current_cell << output_offset

                output_offset = output_offset + 4

            index += 1

        if index < 4:
            offset  = 4 * index
            result |= ((row & (15 << offset)) >> offset) << output_offset

        reversed_result = reverse_row(result)
        reversed_row    = reverse_row(row)

        move_lookup_table[Action.move_up, row] = \
            unpack_column(row) ^ unpack_column(result)

        move_lookup_table[Action.move_down, reversed_row] = \
            unpack_column(reversed_row) ^ unpack_column(reversed_result)

        move_lookup_table[Action.move_left, row] = \
            row ^ result

        move_lookup_table[Action.move_right, reversed_row] = \
            reversed_row ^ reversed_result

    return move_lookup_table

def _initialize_score_lookup_table():
    score_lookup_table = numpy.zeros(
        numpy.iinfo(numpy.uint16).max + 1, dtype=float)

    for row in range(numpy.iinfo(numpy.uint16).max + 1):
        score = 0.0
        for i in range(4):
            rank = (row >> (4 * i)) & 0b1111
            if rank >= 2:
                score += (rank - 1) * (1 << rank)
        score_lookup_table[row] = score

    return score_lookup_table

def _transpose_board_state(board_state):
    board_state = int(board_state)
    a1 = board_state & 0xF0F00F0FF0F00F0F
    a2 = board_state & 0x0000F0F00000F0F0
    a3 = board_state & 0x0F0F00000F0F0000
    a  = a1 | (a2 << 12) | (a3 >> 12)
    b1 = a & 0xFF00FF0000FF00FF
    b2 = a & 0x00FF00FF00000000
    b3 = a & 0x00000000FF00FF00
    return b1 | (b2 >> 24) | (b3 << 24)

class Board(object):
    @staticmethod
    def value_from_raw(value):
        return 2 ** value if value else 0

    @staticmethod
    def value_to_raw(number):
        return int(math.log(number, 2)) if number else 0

    @staticmethod
    def from_matrix(matrix):
        board = Board()
        for row, row_value in enumerate(matrix):
            for column, column_value in enumerate(row_value):
                board.set_value(row, column, column_value)
        return board

    __heuristic_lookup_table = _initialize_heuristic_lookup_table()
    __move_lookup_table      = _initialize_move_lookup_table()
    __score_lookup_table     = _initialize_score_lookup_table()

    __slots__ = ['__state']

    def __init__(self, initializer=0):
        self.__state = initializer

    def __eq__(self, other):
        return self.__state == other.__state

    def __hash__(self):
        return self.__state

    def __str__(self):
        return '\n'.join(
            ''.join('{0:5d}'.format(self.get_value(row, column)) for column in range(4))
            for row in range (4))

    def available(self):
        return [ (row, column)
                 for row in range(4)
                 for column in range(4)
                 if not self.get_value(row, column) ]

    def copy(self):
        return Board(self.__state)

    def get_highest_value(self):
        return max(self.get_value(row, column)
                   for row in range(4)
                   for column in range(4))

    def get_raw_value(self, row, column):
        return 0b1111 & (self.__state >> (0b10000 * row + 0b100 * column))

    def get_value(self, row, column):
        return Board.value_from_raw(self.get_raw_value(row, column))

    def heuristic(self):
        state = self.__state
        transposed_state = _transpose_board_state(state)

        return (Board.__heuristic_lookup_table[(state >>  0) & 0xFFFF] +
                Board.__heuristic_lookup_table[(state >> 16) & 0xFFFF] +
                Board.__heuristic_lookup_table[(state >> 32) & 0xFFFF] +
                Board.__heuristic_lookup_table[(state >> 48) & 0xFFFF] +
                Board.__heuristic_lookup_table[(transposed_state >>  0) & 0xFFFF] +
                Board.__heuristic_lookup_table[(transposed_state >> 16) & 0xFFFF] +
                Board.__heuristic_lookup_table[(transposed_state >> 32) & 0xFFFF] +
                Board.__heuristic_lookup_table[(transposed_state >> 48) & 0xFFFF])

    def move(self, action):
        state = self.__state
        if action is Action.move_up or action is Action.move_down:
            transposed = _transpose_board_state(self.__state)
            return Board(state ^
                (Board.__move_lookup_table[action, (transposed >>  0) & 0xFFFF] <<  0) ^
                (Board.__move_lookup_table[action, (transposed >> 16) & 0xFFFF] <<  4) ^
                (Board.__move_lookup_table[action, (transposed >> 32) & 0xFFFF] <<  8) ^
                (Board.__move_lookup_table[action, (transposed >> 48) & 0xFFFF] << 12))
        else:
            return Board(state ^
                (Board.__move_lookup_table[action, (state >>  0) & 0xFFFF] <<  0) ^
                (Board.__move_lookup_table[action, (state >> 16) & 0xFFFF] << 16) ^
                (Board.__move_lookup_table[action, (state >> 32) & 0xFFFF] << 32) ^
                (Board.__move_lookup_table[action, (state >> 48) & 0xFFFF] << 48))

    def raw(self):
        return self.__state

    def score(self):
        state = self.__state
        return (Board.__score_lookup_table[(state >>  0) & 0xFFFF] +
                Board.__score_lookup_table[(state >> 16) & 0xFFFF] +
                Board.__score_lookup_table[(state >> 32) & 0xFFFF] +
                Board.__score_lookup_table[(state >> 48) & 0xFFFF])

    def set_raw_value(self, row, column, raw_value):
        offset = 0b10000 * row + 0b100 * column
        self.__state = (self.__state & ~(0b1111 << offset)) | (raw_value << offset)

    def set_value(self, row, column, value):
        self.set_raw_value(row, column, Board.value_to_raw(value))

    def spawn(self, row, column, value):
        new_board = Board(self.__state)
        new_board.set_value(row, column, value)
        return new_board

    def to_matrix(self):
        return [ [ self.get_value(row, column) for column in range(4) ]
                 for row in range (4) ]
