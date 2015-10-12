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
        def do_move(column, row):
            index = 0
            output_offset = 16 * row + 4 * column

            while row < 4:
                offset       = 16 * row + 4 * column
                current_cell = (starting_state & (15 << offset)) >> offset

                if current_cell:
                    next_cell = (starting_state & (15 << offset + 16)) >> (offset + 16)

                    if current_cell == next_cell:
                        result_state = result_state | ((current_cell + 1) << output_offset)
                        row = row + 1
                    else:
                        result_state = result_state | (current_cell << output_offset)

                    output_offset = output_offset + 16

                row = row + 1

        starting_state = self.__state
        result_state   = 0

        if action is Action.move_up:
            for column in range(4):
                row = 0
                output_offset = 4 * column

                while row < 4:
                    offset       = 16 * row + 4 * column
                    current_cell = (starting_state & (15 << offset)) >> offset

                    if current_cell:
                        next_cell = (starting_state & (15 << offset + 16)) >> (offset + 16)

                        if current_cell == next_cell:
                            result_state = result_state | ((current_cell + 1) << output_offset)
                            row = row + 1
                        else:
                            result_state = result_state | (current_cell << output_offset)

                        output_offset = output_offset + 16

                    row = row + 1

        return State(result_state)

    def __str__(self):
        return '\n'.join(
            ''.join('{0:5d}'.format(self.get(row, column)) for column in range(4))
            for row in range (4))

    def to_list(self):
        return [ [ self.get(row, column) for column in range(4) ] for row in range (4) ]
