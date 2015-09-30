import collections
import re

import vi.graph

VertexPoint     = collections.namedtuple('VertexPoint', ['i', 'x', 'y'])
GraphBoundaries = collections.namedtuple('Boundaries', ['min', 'max', 'diff'])

def build_vertex_coloring_problem_from_file(filename, k=None):
    k = k or get_k_from_filename(filename)

    with open(filename, 'r') as f:
        graph = parse_graph_file(f.read())

    boundaries = get_graph_boundaries(graph)

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

    domains = { variable: range(1, k + 1)
                for variable in variables.values() }

    network = vi.csp.Network(set(variables.values()), domains, constraints)
    problem = vi.search.gac.Problem(network)

    return problem, k, boundaries

def get_k_from_filename(filename):
    m = re.search('-([0-9])-', filename)
    # Default to 4 if no match found:
    return int(m.group(1)) if m else 4

def get_graph_boundaries(graph):
    min_x = min(vertex.value.x for vertex in graph.vertices)
    max_x = max(vertex.value.x for vertex in graph.vertices)
    min_y = min(vertex.value.y for vertex in graph.vertices)
    max_y = max(vertex.value.y for vertex in graph.vertices)

    diff_x = max_x - min_x
    diff_y = max_y - min_y

    return GraphBoundaries(
        VertexPoint(-1, min_x, min_y),
        VertexPoint(-1, max_x, max_y),
        VertexPoint(-1, diff_x, diff_y))

def parse_graph_file(text):
    def build_vertex(text):
        parts = text.strip().split()
        return vi.graph.Vertex(value=VertexPoint(int(
            parts[0]), float(parts[1]), float(parts[2])))

    def build_edge(text, vertices):
        a_index, b_index = map(int, text.strip().split())
        a, b = vertices[a_index], vertices[b_index]
        edge = vi.graph.Edge(a, b)
        a.edges.add(edge)
        b.edges.add(edge)
        return edge

    lines = text.splitlines()
    num_vertices, num_edges = map(int, lines[0].strip().split())

    vertices = [build_vertex(v) for v in lines[1:1+num_vertices]]
    edges    = [build_edge(e, vertices)
                for e in lines[1+num_vertices:1+num_vertices+num_edges]]

    return vi.graph.Graph(vertices, edges)
