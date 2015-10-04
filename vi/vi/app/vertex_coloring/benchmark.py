import sys

import vi.app.vertex_coloring
import vi.csp
import vi.graph
import vi.search.graph
import vi.search.gac


color_to_text = {
    1: "PINK",
    2: "RED",
    3: "ORANGE",
    4: "GREEN",
    5: "BLUE",
    6: "PURPLE"
}

def update_search_state(state, info):
    def format_node(n):
        if not n.action:
            return "START"
        else:
            return "Vertex{0} is {1}".format(
                n.action[0].identity.value[0],
                color_to_text[n.action[1]])

    #if state == vi.search.graph.State.start:
    #    print(
    #        "Starting search node has state ({0},{1}).".format(
    #            info[0].state.x, info[0].state.y))
    #elif state == vi.search.graph.State.success:
    #    print(
    #        "Success! Solution path to goal state ({0},{1}) with cost {2} was found.".format(
    #            info[0].state.x, info[0].state.y,
    #            info[1].cost))
    if state == vi.search.graph.State.failed:
        print(
            "Failure! No solution could be found.")
    elif state == vi.search.graph.State.expand_node_begin:
        print(
            "Expanding node with assumption {0}.".format(
                format_node(info[0])))
    elif state == vi.search.graph.State.generate_nodes:
        node, successor, is_unique = info
        print(
            "Generated {0} successor state assuming {1} from node with assumption {2}".format(
                "unique" if is_unique else "existing",
                format_node(successor),
                format_node(node)))
    elif state == vi.search.graph.State.expand_node_complete:
        print(
            "Expansion of node with assumption {0} completed.".format(
                format_node(info[0])))


with open(sys.argv[1], 'r') as f:
    graph = vi.app.vertex_coloring.parse_graph_file(f.readlines())

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

    domains = { variable: range(1, K+1)
                for variable in variables.values() }

    big_v, big_d = sorted(domains.items(), key=lambda x: len(x[1]))[0]

    domains[big_v] = [1]

    network = vi.csp.Network(set(variables.values()), domains)
    problem = vi.search.gac.Problem(network)
    search = vi.search.graph.BestFirst(problem, vi.search.graph.BestFirst.astar)

    print("file: {0} K: {1}".format(sys.argv[1], sys.argv[2]))

    while not search.is_complete():
        search.step()
        #update_search_state(search.state, search.info)
