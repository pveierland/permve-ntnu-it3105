class Coordinate(object):
    @staticmethod
    def from_string(input):
        return coordinate(*map(int, input.split(',')))

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, y_offset):
        class CoordinateRelativeAccessor(object):
            def __init__(self, origin, y_offset):
                self.origin   = origin
                self.y_offset = y_offset
            
            def __getitem__(self, x_offset):
                return Coordinate(self.origin.x + x_offset,
                                  self.origin.y + self.y_offset)

        return CoordinateRelativeAccessor(self, y_offset)

    def __str__(self):
        return "coordinate(x={0},y={1})".format(self.x, self.y)

    def down(self):
        return coordinate(self.x, self.y - 1)

    def left(self):
        return coordinate(self.x - 1, self.y)

    def right(self):
        return coordinate(self.x + 1, self.y)

    def up(self):
        return coordinate(self.x, self.y + 1)
