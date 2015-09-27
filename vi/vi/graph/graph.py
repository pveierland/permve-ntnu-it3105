import vi.graph

def from_string(input):
    graph = Graph()
    for connection in input:
        graph.link(*connection)
    return graph

class Graph(object):
    def __init__(self, vertices=None, edges=None):
        self.vertices = vertices or set()
        self.edges    = edges    or set()

    def __str__(self):
        return '\n'.join(str(e) for e in self.edges)

    def get_vertex(self, x):
        return x if x is vi.graph.Vertex else self.lookup(x) or self.insert_vertex(x)

    def insert_vertex(self, x):
        v = x if x is vi.graph.Vertex else vi.graph.Vertex(x)
        self.vertices.add(v)
        return v

    def link(self, a, b, cost=None):
        v1 = self.get_vertex(a)
        v2 = self.get_vertex(b)

        e = vi.graph.Edge(v1, v2, cost)
        v1.edges.add(e)
        v2.edges.add(e)
        self.edges.add(e)

        return e

    def lookup(self, predicate):
        if hasattr(predicate, '__call__'):
            matches = filter(predicate, self.vertices)
        else:
            matches = [v for v in self.vertices if v.value == value]
        assert len(matches) <= 1
        return matches[0]
