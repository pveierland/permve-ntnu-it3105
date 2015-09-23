class coordinate(object):
    @staticmethod
    def from_string(input):
        return coordinate(*map(int, input.split(',')))

    def __init__(self, x, y):
        self.x = x
        self.y = y
