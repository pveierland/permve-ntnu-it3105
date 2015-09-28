class Network(object):
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains   = domains

    def shallow_copy(self):
        return Network(self.variables, self.domains)
