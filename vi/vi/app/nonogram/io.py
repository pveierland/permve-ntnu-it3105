import itertools

from vi.grid import Coordinate

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

def parse_file(text):
    lines = text.splitlines()

    dimensions   = Coordinate(*map(int, lines[0].strip().split()))
    row_specs    = [ map(int, line.strip().split()) for line in lines[1:1+dimensions.y] ]
    column_specs = [ map(int, line.strip().split())
                      for line in lines[1+dimensions.y:1+dimensions.x+dimensions.y] ]

    return dimensions, row_specs, column_specs

