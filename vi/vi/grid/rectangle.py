class Rectangle(object):
    @staticmethod
    def from_string(input):
        return Rectangle(*map(int, input.split(',')))

    def __init__(self, x, y, width, height):
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height

    def __eq__(self, other):
        return self.x == other.x and \
               self.y == other.y and \
               self.width == other.width and \
               self.height == other.height

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))

    def __str__(self):
        return "Rectangle(x={0},y={1},width={2},height={3})" \
            .format(self.x, self.y, self.width, self.height)
