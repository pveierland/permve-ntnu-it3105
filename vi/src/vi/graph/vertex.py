class vertex(object):
    def __init__(self, value, edges=None):
        self.value = value
        self.edges = edges or set()

    def __str__(self):
        s = 'vertex'
        if self.value:
            s += ' ' + str(self.value)
        if self.edges:
            for edge in self.edges:
                s += '\n\t' + edge.build_str(self)
        return s
