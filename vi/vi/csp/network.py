class Network(object):
    def __init__(self, variables, domains, constraints):
        self.variables   = variables
        self.domains     = domains
        self.constraints = constraints

    def copy(self):
        return Network(self.variables,
                       self.domains.copy(),
                       self.constraints)
