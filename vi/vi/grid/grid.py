# Value used to indicate that a grid cell is obstructed
obstructed = -1

class Grid(object):
    def __init__(self, width, height):
        self.width  = width
        self.height = height

        # All grid values are initialized to the default cost: 1
        self.values = [ [ 1 for x in range(width) ] for y in range(height) ]

    def __str__(self):
        def format_row(row):
            return ''.join('{0: >3}'.format(element) for element in row)
        return '\n'.join(format_row(row) for row in reversed(self.values))
