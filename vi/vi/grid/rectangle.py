class rectangle(object):
    @staticmethod
    def from_string(input):
        return rectangle(*map(int, input.split(',')))

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width  = width
        self.height = height
