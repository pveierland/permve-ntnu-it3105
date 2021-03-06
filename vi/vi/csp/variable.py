class Variable(object):
    def __init__(self, identity, constraints = None):
        self.identity    = identity
        self.constraints = constraints or set()

    def __eq__(self, other):
        return self.identity == (other.identity if other is Variable else other)

    def __hash__(self):
        return hash(self.identity)

    def __str__(self):
        return "Variable({0})".format(self.identity)
