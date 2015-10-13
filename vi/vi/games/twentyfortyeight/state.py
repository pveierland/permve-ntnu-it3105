import math

from vi.search.grid import Action

class State(object):
    @staticmethod
    def convert_compact_value_to_number(value):
        return 2 ** value if value else 0

    @staticmethod
    def convert_number_to_compact_value(number):
        return int(math.log(number, 2)) if number else 0

    @classmethod
    def from_matrix(cls, matrix):
        state = cls()
        for row, row_value in enumerate(matrix):
            for column, column_value in enumerate(row_value):
                state.set_value(row, column, column_value)
        return state

    __slots__ = ['__state']

    def __init__(self, initializer=0):
        self.__state = initializer
    
    def __str__(self):
        return '\n'.join(
            ''.join('{0:5d}'.format(self.get_number(row, column)) for column in range(4))
            for row in range (4))
        
    def available(self):
        return [ (row, column)
                 for row in range(4)
                 for column in range(4)
                 if not self.get_number(row, column) ]

    def copy(self):
        return State(self.__state)

    def get_highest_value(self):
        return max(self.get_number(row, column)
                   for row in range(4)
                   for column in range(4))

    def get_number(self, row, column):
        return State.convert_compact_value_to_number(self.get_value(row, column))
    
    def get_value(self, row, column):
        return 15 & (self.__state >> (16 * row + 4 * column))

    def move(self, action):
        def do_move(starting_state, start_offset, separator):
            result_state  = 0
            output_offset = start_offset

            index = 0
            while index < 3:
                offset       = separator * index + start_offset
                current_cell = (starting_state & (15 << offset)) >> offset

                if current_cell:
                    next_cell = (starting_state & (15 << (offset + separator))) >> (offset + separator)

                    if current_cell == next_cell:
                        result_state = result_state | ((current_cell + 1) << output_offset)
                        index = index + 1
                    else:
                        result_state = result_state | (current_cell << output_offset)

                    output_offset = output_offset + separator

                index = index + 1

            if index < 4:
                offset       = separator * index + start_offset
                result_state = result_state | (((starting_state & (15 << offset)) >> offset) << output_offset)

            return result_state

        starting_state = self.__state
        result_state   = 0

        if action is Action.move_up:
            for column in range(4):
                result_state = result_state | do_move(starting_state, 4 * column, 16)
        elif action is Action.move_down:
            for column in range(4):
                result_state = result_state | do_move(starting_state, 48 + 4 * column, -16)
        elif action is Action.move_left:
            for row in range(4):
                result_state = result_state | do_move(starting_state, 16 * row, 4)
        elif action is Action.move_right:
            for row in range(4):
                result_state = result_state | do_move(starting_state, 16 * row + 12, -4)

        return State(result_state)
    
    def set_value(self, row, column, value):
        self.__state = self.__state | (State.convert_number_to_compact_value(value) << (16 * row + 4 * column))
        return self

    def to_matrix(self):
        return [ [ self.get_number(row, column) for column in range(4) ] for row in range (4) ]
