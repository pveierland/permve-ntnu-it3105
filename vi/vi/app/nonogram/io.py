from enum import Enum

import collections
import itertools
import sys

import vi.csp
import vi.search.gac

class Dimension(Enum):
    column = 1
    row    = 2

def veritas(values, row_variable, column_variable, row_index, column_index):
    print("VERITAS row_variable={0} column_variable={1} row_index={2} column_index={3} values={4}".format(
        row_variable.identity, column_variable.identity, row_index, column_index, ''.join('{0}:{1}'.format(a.identity, b) for a, b in values.items())))
    truth = ((values[row_variable] & row_index) != 0) == ((values[column_variable] & column_index) != 0)

    print("TRUE" if truth else "FALSE")
    return truth

def build_constraints(row_variables, column_variables, row_domains, column_domains, width, height):
    constraints = []

    for row, row_domain in enumerate(row_domains):
        for column, column_domain in enumerate(column_domains):
            constraint = vi.csp.Constraint(
                [row_variables[row], column_variables[column]],
                lambda values,
                       row_variable=row_variables[row],
                       column_variable=column_variables[column],
                       row_index=(1 << (width - column - 1)),
                       column_index=(1 << row):
                    ((values[row_variable] & row_index) != 0) == \
                    ((values[column_variable] & column_index) != 0))

            #veritas(values, row_variable, column_variable, row_index, column_index))

            row_variables[row].constraints.add(constraint)
            column_variables[column].constraints.add(constraint)
            constraints.append(constraint)

    return constraints




#    constraints = {}
#
#    print("COLUMN DOMAINS")
#
#    for cd in column_domains:
#        print(' '.join('{0:b}'.format(c) for c in cd))
#
#    print()
#    print("ROW DOMAINS")
#
#    for rd in row_domains:
#        print(' '.join('{0:b}'.format(r) for r in rd))
#
#    print()
#    print()
#
#    for row, row_domain in enumerate(row_domains):
#        # Use basic calculation to get superset of needed constraints:
#        s = 0
#        for r in range(0, len(row_domain)):
#            s = s ^ row_domain[r]
#
#        for column in range(width):
#            if s & (1 << (width - column - 1)) != 0:
#                if not (row, column) in constraints:
#                    constraint = vi.csp.Constraint(
#                        [row_variables[row], column_variables[column]],
#                        lambda values,
#                               row_variable=row_variables[row],
#                               column_variable=column_variables[column],
#                               row_index=(1 << (width - column - 1)),
#                               column_index=(1 << row):
#                            ((values[row_variable] & row_index) != 0) == \
#                            ((values[column_variable] & column_index) != 0))
#
##veritas(values, row_variable, column_variable, row_index, column_index))
#
#                    row_variables[row].constraints.add(constraint)
#                    column_variables[column].constraints.add(constraint)
#                    constraints[(row, column)] = constraint
#
#    for column, column_domain in enumerate(column_domains):
#        # Use basic calculation to get superset of needed constraints:
#        s = 0
#        for r in range(0, len(column_domain)):
#            s = s ^ column_domain[r]
#
#        for row in range(height):
#            if s & (1 << row) != 0:
#                if not (row, column) in constraints:
#                    print("LINK row={0} with column={1}".format(row, column))
#                    constraint = vi.csp.Constraint(
#                        [column_variables[column], row_variables[row]],
#                        lambda values,
#                               column_variable=column_variables[column],
#                               row_variable=row_variables[row],
#                               column_index=(1 << row),
#                               row_index=(1 << (width - column - 1)):
#                            ((values[row_variable] & row_index) != 0) == \
#                            ((values[column_variable] & column_index) != 0))
##                            veritas(values, row_variable, column_variable, row_index, column_index))
#
#
#                    column_variables[column].constraints.add(constraint)
#                    row_variables[row].constraints.add(constraint)
#                    constraints[(row, column)] = constraint
#    
#    #print("TRY TO STOP ME!")
#    #for constraint in constraints:
#    #    print(' + '.join(variable.identity for variable in constraint.variables))
#
#    return constraints.values()

def build_domain(dimension, spec):
    def build_pattern(m):
        pattern = 0

        for one, zero in zip(spec, m):
            pattern = pattern << (one + zero + 1)
            pattern = pattern | ((1 << one) - 1)

        pattern = pattern << m[-1]
        return pattern

    return [build_pattern(m) for m in multichoose(len(spec) + 1, dimension - sum(spec) - len(spec) + 1)]

def build_problem(text):
    dimensions, row_specs, column_specs = parse_file(text)

    row_domains = [ list(build_domain(dimensions[0], row_spec))
                    for row_spec in row_specs ]

    column_domains = [ list(build_domain(dimensions[1], column_spec))
                       for column_spec in column_specs ]

    row_values = sum(len(row_domain) for row_domain in row_domains)
    column_values = sum(len(column_domain) for column_domain in column_domains)

    print("\nrow_values = {0}, column_values = {1}".format(row_values, column_values))

#    for row in range(len(row_domains)):
#        for column, column_domain in enumerate(column_domains):
#            row_domains[row] = reduce_row_domain(row_domains[row], column_domain, row, column, dimensions[0], dimensions[1])
#
#    for column in range(len(column_domains)):
#        for row, row_domain in enumerate(row_domains):
#            column_domains[column] = reduce_column_domain(row_domain, column_domains[column], row, column, dimensions[0], dimensions[1])

    row_values = sum(len(row_domain) for row_domain in row_domains)
    column_values = sum(len(column_domain) for column_domain in column_domains)

    print("\nrow_values = {0}, column_values = {1}".format(row_values, column_values))

    row_variables    = [ vi.csp.Variable((Dimension.row, row)) for row in range(dimensions[1]) ]
    column_variables = [ vi.csp.Variable((Dimension.column, column)) for column in range(dimensions[0]) ]

    variables = row_variables + column_variables

    domains = {}

    domains.update({
        row_variables[row]: row_domain
        for row, row_domain in enumerate(row_domains) })

    domains.update({
        column_variables[column]: column_domain
        for column, column_domain in enumerate(column_domains) })

    constraints = build_constraints(row_variables, column_variables, row_domains, column_domains, dimensions[0], dimensions[1])

    network = vi.csp.Network(variables, domains, constraints)
    problem = vi.search.gac.Problem(network)

    return problem, dimensions

# http://mathoverflow.net/a/9494
def multichoose(n,k):
    if k < 0 or n < 0: return "Error"
    if not k: return [[0]*n]
    if not n: return []
    if n == 1: return [[k]]
    return [[0]+val for val in multichoose(n-1,k)] + \
           [[val[0]+1]+val[1:] for val in multichoose(n,k-1)]

def parse_file(text):
    lines = text.splitlines()

    dimensions   = list(map(int, lines[0].strip().split()))
    row_specs    = [ list(map(int, line.strip().split()))
                     for line in lines[1:1+dimensions[1]] ]
    column_specs = [ list(map(int, line.strip().split()))
                     for line in lines[1+dimensions[1]:1+dimensions[0]+dimensions[1]] ]

    return dimensions, row_specs, column_specs

def reduce_column_domain(row_domain, column_domain, row, column, width, height):
    if all(row_values & (1 << (width - column - 1)) != 0 for row_values in row_domain):
        return [column_values for column_values in column_domain if column_values & (1 << row) != 0]
    elif not any(row_values & (1 << (width - column - 1)) != 0 for row_values in row_domain):
        return [column_values for column_values in column_domain if not column_values & (1 << row) != 0]
    else:
        return column_domain

def reduce_row_domain(row_domain, column_domain, row, column, width, height):
    if all(column_values & (1 << row) != 0 for column_values in column_domain):
        return [row_values for row_values in row_domain if row_values & (1 << width - column - 1) != 0]
    elif not any(column_values & (1 << row) != 0 for column_values in column_domain):
        return [row_values for row_values in row_domain if not row_values & (1 << width - column - 1) != 0]
    else:
        return row_domain
