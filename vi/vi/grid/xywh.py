class xywh(object):
    @staticmethod
    def from_string(input):
        return xywh(*map(int, input.split(',')))

    def __init__(self, x, y, width, height):
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height
