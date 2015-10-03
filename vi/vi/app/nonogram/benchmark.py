import sys

import vi.app.nonogram
import vi.csp
import vi.graph
import vi.search.graph
import vi.search.gac

with open(sys.argv[1], 'r') as f:
    problem = vi.app.nonogram.build_problem(f.read())

search = vi.search.graph.AStar(problem)

while not search.is_complete():
    search.step()
