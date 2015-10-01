import itertools
import sys

def build_domain(dimension, spec):
    def satisfies(state, spec):
        truths = 0
        s      = 0

        for index, value in enumerate(state):
            if value:
                truths = truths + 1

            segment_complete = (not value) or (index == len(state) - 1)

            if segment_complete:
                segment_is_match = s != len(spec) and truths == spec[s]

                if segment_is_match:
                    s = s + 1
                    truths = 0
                elif truths != 0:
                    return False

        return s == len(spec) and truths == 0

    return [ state
             for state in itertools.product([False, True], repeat=dimension)
             if satisfies(state, spec) ]

def build_problem(text):
    dimensions, row_specs, column_specs = parse_file(text)

    print(dimensions)

    row_domains = [ build_domain(dimensions[0], row_spec)
                    for row_spec in row_specs ]

    column_domains = [ build_domain(dimensions[1], column_spec)
                       for column_spec in column_specs ]
    
    row_values = sum(len(row_domain) for row_domain in row_domains)
    column_values = sum(len(column_domain) for column_domain in column_domains)

    print("\nrow_values = {0}, column_values = {1}".format(row_values, column_values))

    for row in range(len(row_domains)):
        for column, column_domain in enumerate(column_domains):
            before = row_domains[row]
            row_domains[row] = reduce_domain(row_domains[row], column_domain, column, row)
            if not row_domains[row]:
                print("WTF")
                print("{0} {1}".format(column, row))
                print(before)
                print(column_domain)
                return

    for column in range(len(column_domains)):
        for row, row_domain in enumerate(row_domains):
            column_domains[column] = reduce_domain(column_domains[column], row_domain, row, column)

    row_values = sum(len(row_domain) for row_domain in row_domains)
    column_values = sum(len(column_domain) for column_domain in column_domains)

    print("\nrow_values = {0}, column_values = {1}".format(row_values, column_values))

def parse_file(text):
    lines = text.splitlines()

    dimensions   = list(map(int, lines[0].strip().split()))
    row_specs    = [ list(map(int, line.strip().split())) for line in lines[1:1+dimensions[1]] ]
    column_specs = [ list(map(int, line.strip().split()))
                     for line in lines[1+dimensions[1]:1+dimensions[0]+dimensions[1]] ]

    return dimensions, row_specs, column_specs

def reduce_domain(domain_a, domain_b, index_a, index_b):
    #print("{0} {1} {2} {3}".format(index_a, len(domain_a[0]), index_b, len(domain_b[0])))
    if len(domain_a) == 0 or len(domain_b) == 0:
        print("REDUCE {0} {1}".format(len(domain_a), len(domain_b)))
        print("{0} {1}".format(index_a, index_b))
        sys.exit(1)
    #print("{0} {1} {2} {3}".format(index_a, len(domain_a[0]), index_b, len(domain_b[0])))
    if all(b[index_b] for b in domain_b):
        print("ALL")
        return [a for a in domain_a if a[index_a]]
    elif not any(b[index_b] for b in domain_b):
        print("NONE")
        return [a for a in domain_a if not a[index_a]]
    else:
        print("WHATEVER")
        return domain_a
