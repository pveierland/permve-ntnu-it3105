class Constraint(object):
    @staticmethod
    def constrain(variables, condition):
        constraint = Constraint(variables, condition)
        for variable in variables:
            variable.constraints.add(constraint)
        return constraint

    def __init__(self, variables, condition):
        self.variables = variables
        self.condition = condition

    def __call__(self, values):
        return self.condition(values)
