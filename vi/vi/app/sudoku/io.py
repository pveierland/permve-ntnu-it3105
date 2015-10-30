import itertools
import numpy

from vi.csp import Constraint, Network, Variable

def build_binary_constraints(variables):
    def build_binary_constraint_combinations(variables, condition):
        return [ Constraint.constrain(variable_pair, condition)
                for variable_pair in itertools.combinations(variables, 2) ]

    def is_different(values):
        a, b = values.values()
        return a != b

    constraints = []

    for row in range(9):
        constraints.extend(build_binary_constraint_combinations(
            variables[row,:], is_different))

    for column in range(9):
        constraints.extend(build_binary_constraint_combinations(
            variables[:,column], is_different))

    for row_group in range(3):
        for column_group in range(3):
            group_variables = variables[ \
                row_group    * 3:(row_group + 1)    * 3,
                column_group * 3:(column_group + 1) * 3].flatten()

            constraints.extend(build_binary_constraint_combinations(
                group_variables, is_different))

    return constraints

def build_general_constraints(variables):
    def all_unique(values):
        x = 0
        for value in values.values():
            if value:
                z = (1 << value)
                if (x & z) != 0:
                    return False
                x = x | z
        return True

    constraints = []

    for row in range(9):
        constraints.append(Constraint.constrain(variables[row,:], all_unique))

    for column in range(9):
        constraints.append(Constraint.constrain(variables[:,column], all_unique))

    for row_group in range(3):
        for column_group in range(3):
            group_variables = variables[ \
                row_group    * 3:(row_group + 1)    * 3,
                column_group * 3:(column_group + 1) * 3].flatten()

            constraints.append(Constraint.constrain(group_variables, all_unique))

    return constraints

def build_network(puzzle, use_general_constraints):
    domains   = {}
    variables = numpy.empty((9, 9), dtype=object)

    for row in range(9):
        for column in range(9):
            variable = Variable((row, column))
            variables[(row, column)] = variable

            value = puzzle[row, column]

            if value:
                domains[variable] = [value]
            else:
                row_values    = puzzle[row,:]
                column_values = puzzle[:,column]
                group_values  = puzzle[ \
                    (row // 3)    * 3:((row // 3) + 1)    * 3,
                    (column // 3) * 3:((column // 3) + 1) * 3].flatten()

                domains[variable] = [ x for x in range(1, 10) \
                                      if x not in row_values and \
                                         x not in column_values and \
                                         x not in group_values ]

    constraints = build_general_constraints(variables) \
                  if use_general_constraints \
                  else build_binary_constraints(variables)

    return Network(list(variables.flatten()), domains, constraints)

def convert_network_to_puzzle(network):
    puzzle = numpy.zeros((9, 9), dtype=int)

    for variable in network.variables:
        row, column         = variable.identity
        puzzle[row, column] = network.domains[variable][0] \
                              if len(network.domains[variable]) == 1 else 0

    return puzzle

def load_network(filename, use_general_constraints):
    return build_network(load_puzzle(filename), use_general_constraints)

def load_puzzle(filename):
    puzzle = numpy.zeros((9, 9), dtype=int)

    with open(filename) as input_file:
        for row, row_values in enumerate(input_file.read().splitlines()):
            for column, column_value in enumerate(row_values):
                puzzle[row, column] = int(column_value)

    return puzzle
