class vertex(object):
    def __init__(self, value, edges=[]):
        self.value = value
        self.edges = edges

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)
