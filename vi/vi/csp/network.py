class Network(object):
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains   = domains

    def copy(self):
        return Network(self.variables.copy(),
                       self.domains.copy())
