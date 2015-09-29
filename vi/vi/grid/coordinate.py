class Coordinate(object):
    @staticmethod
    def from_string(input):
        return Coordinate(*map(int, input.split(',')))

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

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
        return "Coordinate(x={0},y={1})".format(self.x, self.y)

    def down(self):
        return Coordinate(self.x, self.y - 1)

    def left(self):
        return Coordinate(self.x - 1, self.y)

    def right(self):
        return Coordinate(self.x + 1, self.y)

    def up(self):
        return Coordinate(self.x, self.y + 1)
