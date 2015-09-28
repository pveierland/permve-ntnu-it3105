class Variable(object):
    def __init__(self, identity, constraints = None):
        self.identity    = identity
        self.constraints = constraints

    def __eq__(self, other):
        return self.identity == other.identity

    def __hash__(self):
        return hash(self.identity)

    def __str__(self):
        return "Variable({0})".format(self.identity)
