class wh(object):
    @staticmethod
    def from_string(input):
        return wh(*map(int, input.split(',')))

    def __init__(self, w, h):
        self.w = w
        self.h = h
