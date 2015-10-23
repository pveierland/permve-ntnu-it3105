import math
import numpy

from vi.search.grid import Action

def _initialize_move_lookup_table():
    def reverse_row(row):
        return ((row & 0xF000) >> 12) | ((row & 0x0F00) >> 4) | \
               ((row & 0x000F) << 12) | ((row & 0x00F0) << 4)

    def unpack_column(row):
        return (row | (row << 12) | (row << 24) | (row << 36)) & 0x000F000F000F000F

    move_lookup_table = numpy.zeros(
        (4, numpy.iinfo(numpy.uint16).max + 1), dtype=numpy.uint16)

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

def _transpose_board_state(board_state):
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

    __move_lookup_table = _initialize_move_lookup_table()
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

    def move(self, action):
        if action is Action.move_up or action is Action.move_down:
            state = _transpose_board_state(self.__state)
            
            print("WOOT! {0}".format(Board.__move_lookup_table[action, (state >> 0) & 0xFFFF]))

            return Board(state ^
                (Board.__move_lookup_table[action, (state >>  0) & 0xFFFF] <<  0) ^
                (Board.__move_lookup_table[action, (state >> 16) & 0xFFFF] <<  4) ^
                (Board.__move_lookup_table[action, (state >> 32) & 0xFFFF] <<  8) ^
                (Board.__move_lookup_table[action, (state >> 48) & 0xFFFF] << 12))
        else:
            state = self.__state

            return Board(state ^
                (Board.__move_lookup_table[action, (state >>  0) & 0xFFFF] <<  0) ^
                (Board.__move_lookup_table[action, (state >> 16) & 0xFFFF] << 16) ^
                (Board.__move_lookup_table[action, (state >> 32) & 0xFFFF] << 32) ^
                (Board.__move_lookup_table[action, (state >> 48) & 0xFFFF] << 48))

    def set_raw_value(self, row, column, raw_value):
        offset = 0b10000 * row + 0b100 * column
        self.__state = (self.__state & ~(0b1111 << offset)) | (raw_value << offset)

    def set_value(self, row, column, value):
        self.set_raw_value(row, column, Board.value_to_raw(value))

    def to_matrix(self):
        return [ [ self.get_value(row, column)
                   for column in range(4) ]
                 for row in range (4) ]
