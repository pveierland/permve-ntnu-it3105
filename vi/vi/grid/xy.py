class xy(object):
    @staticmethod
    def from_string(input):
        return xy(*map(int, input.split(',')))

    def __init__(self, x, y):
        self.x = x
        self.y = y
