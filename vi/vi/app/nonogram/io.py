import collections
import itertools
import sys

#def build_domain(dimension, spec):
#    def satisfies(state, spec):
#        truths = 0
#        s      = 0
#
#        for index, value in enumerate(state):
#            if value:
#                truths = truths + 1
#
#            segment_complete = (not value) or (index == len(state) - 1)
#
#            if segment_complete:
#                segment_is_match = s != len(spec) and truths == spec[s]
#
#                if segment_is_match:
#                    s = s + 1
#                    truths = 0
#                elif truths != 0:
#                    return False
#
#        return s == len(spec) and truths == 0
#
#    return [ state
#             for state in itertools.product([False, True], repeat=dimension)
#             if satisfies(state, spec) ]

#def build_domain(dimension, spec):
#    def satisfies(state, spec):
#        truths = 0
#        s      = 0
#
#        for index, value in enumerate(state):
#            if value:
#                truths = truths + 1
#
#            segment_complete = (not value) or (index == len(state) - 1)
#
#            if segment_complete:
#                segment_is_match = s != len(spec) and truths == spec[s]
#
#                if segment_is_match:
#                    s = s + 1
#                    truths = 0
#                elif truths != 0:
#                    return False
#
#        return s == len(spec) and truths == 0
#
#    return [ state
#             for state in itertools.product([False, True], repeat=dimension)
#             if satisfies(state, spec) ]

#def is_valid_pattern(dimension, spec, pattern):
#    num_specs = len(spec)
#    s = 0
#    i = dimension - 1
#
#    #print("SATISFY THIS! dimension={0} spec={1} pattern={2}", dimension, spec, pattern)
#
#    while True:
#        #input("Press Enter to continue...")
#        #print('i={0}'.format(i))
#        if pattern & (1 << i) != 0:
#            #print('{0:b} is ONE'.format(pattern))
#            l = spec[s]
#            for j in range(1, l):
#                if pattern & (1 << (i - j)) == 0:
#                    ##print("ALPHA")
#                    return False
#            else:
#                ##print('i={0} j={1}'.format(i, j))
#                if i > l - 1 and pattern & (1 << (i - l)) != 0:
#                    return False
#
#                i = i - l - 1
#                s = s + 1
#
#                if s == num_specs:
#                    break
#        else:
#            if i == 0:
#                break
#            else:
#                i = i - 1
#
#    if i > 0 and pattern & ((1 << i) - 1) != 0:
#        ##print("BOOM")
#        return False
#
#    return s == num_specs
#
#def build_domain(dimension, spec):
#    # Build first valid bit pattern:
#    num_specs = len(spec)
#    pattern   = (1 << spec[0]) - 1
#
#    for s in spec[1:]:
#        pattern = pattern << (s + 1)
#        pattern = pattern | ((1 << s) - 1)
#
#    while pattern & (1 << dimension) == 0:
#        s = 0
#        i = dimension - 1
#
#        while True:
#            if pattern & (1 << i) != 0:
#                l = spec[s]
#                for j in range(1, l):
#                    if pattern & (1 << (i - j)) == 0:
#                        is_valid = False
#                        break
#                else:
#                    if i > l - 1 and pattern & (1 << (i - l)) != 0:
#                        is_valid = False
#                        break
#
#                    i = i - l - 1
#                    s = s + 1
#
#                    if s == num_specs:
#                        break
#            else:
#                if i == 0:
#                    break
#                else:
#                    i = i - 1
#
#        if i > 0 and pattern & ((1 << i) - 1) != 0:
#            ##print("BOOM")
#            return False
#
#        return s == num_specs
#
#
#    # TEST BIN STRATEGY OR SUCK IT UP
#
#
#
#
#
#
#
#
#        if is_valid_pattern(dimension, spec, pattern):
#            yield int(pattern)
#
#        # Compute the lexicographically next bit permutation
#        # https://graphics.stanford.edu/~seander/bithacks.html
#        t = (pattern | (pattern - 1)) + 1
#        pattern = t | ((((t & -t) // (pattern & -pattern)) >> 1) - 1)

# http://mathoverflow.net/a/9494
def multichoose(n,k):
    if k < 0 or n < 0: return "Error"
    if not k: return [[0]*n]
    if not n: return []
    if n == 1: return [[k]]
    return [[0]+val for val in multichoose(n-1,k)] + \
           [[val[0]+1]+val[1:] for val in multichoose(n,k-1)]

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

    print(dimensions)

    row_domains = [ list(build_domain(dimensions[0], row_spec))
                    for row_spec in row_specs ]

    column_domains = [ list(build_domain(dimensions[1], column_spec))
                       for column_spec in column_specs ]

    row_values = sum(len(row_domain) for row_domain in row_domains)
    column_values = sum(len(column_domain) for column_domain in column_domains)

    print("\nrow_values = {0}, column_values = {1}".format(row_values, column_values))

    for row in range(len(row_domains)):
        for column, column_domain in enumerate(column_domains):
            row_domains[row] = reduce_domain(row_domains[row], column_domain, column, row, dimensions[0], dimensions[1])

    for column in range(len(column_domains)):
        for row, row_domain in enumerate(row_domains):
            column_domains[column] = reduce_domain(column_domains[column], row_domain, row, column, dimensions[1], dimensions[0])

    row_values = sum(len(row_domain) for row_domain in row_domains)
    column_values = sum(len(column_domain) for column_domain in column_domains)

    print("\nrow_values = {0}, column_values = {1}".format(row_values, column_values))

    find_common(dimensions, row_domains, column_domains)

def parse_file(text):
    lines = text.splitlines()

    dimensions   = list(map(int, lines[0].strip().split()))
    row_specs    = list(reversed(list(list(map(int, line.strip().split())) for line in lines[1:1+dimensions[1]])))
    column_specs = [ list(map(int, line.strip().split()))
                     for line in lines[1+dimensions[1]:1+dimensions[0]+dimensions[1]] ]

    return dimensions, row_specs, column_specs

def reduce_domain(domain_a, domain_b, index_a, index_b, dimension_a, dimension_b):
    if all(b & (1 << (dimension_b - index_b - 1)) != 0 for b in domain_b):
        return [a for a in domain_a if a & (1 << (dimension_a - index_a - 1)) != 0]
    elif not any(b & (1 << (dimension_b - index_b - 1)) != 0 for b in domain_b):
        return [a for a in domain_a if not a & (1 << (dimension_a - index_a - 1)) != 0]
    else:
        return domain_a

def find_common(dimensions, row_domains, column_domains):
    for row, row_domain in enumerate(row_domains):
        row_domain_copy = row_domain.copy()
        constraints = []

        ones  = [[0, []] for dimension in range(dimensions[0])]
        zeros = [[0, []] for dimension in range(dimensions[0])]

        for r in row_domain:
            for n in range(dimensions[0]):
                if r & (1 << (dimensions[0] - n - 1)):
                    ones[n][0] = ones[n][0] + 1
                    ones[n][1].append(r)
                else:
                    zeros[n][0] = zeros[n][0] + 1
                    zeros[n][1].append(r)
            print()
            print()

        print(ones)
        print(zeros)
        input("Press Enter to continue...")

#        min(enumerate(ones)

#omin_index, min_value = min(enumerate(values), key=operator.itemgetter(1))k


