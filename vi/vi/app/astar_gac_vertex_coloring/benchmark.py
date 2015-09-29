import sys

import vi.app.astar_gac_vertex_coloring
import vi.csp
import vi.graph
import vi.search.graph
import vi.search.gac

with open(sys.argv[1], 'r') as f:
    graph = vi.app.astar_gac_vertex_coloring.parse_graph_file(f.readlines())

    variables = { vertice: vi.csp.Variable(vertice)
                  for vertice in graph.vertices }

    constraints = []

    for edge in graph.edges:
        variable_a = variables[edge.a]
        variable_b = variables[edge.b]

        constraint = vi.csp.Constraint([variable_a, variable_b],
            (lambda values, a=variable_a, b=variable_b: \
                values[a] != values[b]))

        variable_a.constraints.add(constraint)
        variable_b.constraints.add(constraint)

        constraints.append(constraint)

    K = int(sys.argv[2])

    domains = { variable: range(1, K)
                for variable in variables.itervalues() }

    network = vi.csp.Network(set(variables.itervalues()), domains)
    problem = vi.search.gac.Problem(network)
    search = vi.search.graph.AStar(problem)

    print("file: {0} K: {1}".format(sys.argv[1], sys.argv[2]))

    while not search.is_complete():
        search.step()

