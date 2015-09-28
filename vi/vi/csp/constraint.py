class Constraint(object):
    def __init__(self, variables, condition):
        self.variables = variables
        self.condition = condition

    def __call__(self, values):
        return self.condition(values)
