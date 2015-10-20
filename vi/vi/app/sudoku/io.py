import numpy

from vi.csp import Constraint, Variable
import vi.search.gac

def load_puzzle(filename):
    puzzle = numpy.zeros((9, 9))

    with open(filename) as input_file:
        for row, row_values in enumerate(input_file.read().splitlines()):
            for column, column_value in enumerate(row_values):
                puzzle[row, column] = int(column_value)

    return puzzle

def build_puzzle(filename)
    puzzle = load_puzzle(filename)

    domains = {}

    for row in range(9):
        for column in range(9):
            variable = Variable('Row{0}Col{1}'.format(row, column))
            domain   = range(9)
            domains[v] = range(9)
            domains

