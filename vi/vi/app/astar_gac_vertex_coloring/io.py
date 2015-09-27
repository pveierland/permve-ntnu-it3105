import vi.graph

def parse_graph_file(lines):
    def build_vertex(text):
        parts = text.strip().split()

        index = int(parts[0])
        x, y  = map(float, parts[1:])

        return vi.graph.Vertex(value=(index, (x, y)))

    def build_edge(text, vertices):
        a_index, b_index = map(int, text.strip().split())
        a, b = vertices[a_index], vertices[b_index]
        edge = vi.graph.Edge(a, b)
        a.edges.add(edge)
        b.edges.add(edge)
        return edge

    num_vertices, num_edges = map(int, lines[0].strip().split())

    vertices = [build_vertex(v) for v in lines[1:1+num_vertices]]
    edges    = [build_edge(e, vertices)
                for e in lines[1+num_vertices:1+num_vertices+num_edges]]

    return vi.graph.Graph(vertices, edges)

