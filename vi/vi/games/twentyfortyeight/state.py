import math

from vi.search.grid import Action

class State(object):
    @staticmethod
    def convert_compact_value_to_number(value):
        return 2 ** value if value else 0

    __slots__ = ['__state']

    def __init__(self, initializer=0):
        if isinstance(initializer, list):
            state = 0
            for row, row_value in enumerate(initializer):
                for column, column_value in enumerate(row_value):
                    if column_value:
                        state = state | (int(math.log(column_value, 2)) << (16 * row + 4 * column))
            self.__state = state
        else:
            self.__state = initializer

    def get(self, row, column):
        return State.convert_compact_value_to_number(15 & (self.__state >> (16 * row + 4 * column)))

    def move(self, action):
        def do_move(starting_state, start_offset, separator):
            result_state  = 0
            output_offset = start_offset

            index = 0
            while index < 4:
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

    def __str__(self):
        return '\n'.join(
            ''.join('{0:5d}'.format(self.get(row, column)) for column in range(4))
            for row in range (4))

    def to_list(self):
        return [ [ self.get(row, column) for column in range(4) ] for row in range (4) ]
