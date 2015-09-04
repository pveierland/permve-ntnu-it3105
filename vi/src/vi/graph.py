from edge import *
from vertex import *

class graph(object):
    def __init__(self, vertices=set(), edges=set()):
        self.vertices = vertices if not vertices else\
            set([ x if x is vertex else vertex(x) for x in vertices ])
        self.edges = edges

    def get_vertex(self, x):
        return x if x is vertex else self.lookup(x) or self.insert_vertex(x)

    def insert_vertex(self, x):
        v = x if x is vertex else vertex(x)
        self.vertices.add(v)
        return v
    
    def link(self, a, b, cost=None):
        v1 = self.get_vertex(a)
        v2 = self.get_vertex(b)
        self.edges.add(edge(v1, v2, cost))

    def lookup(self, value):
        return next((v for v in self.vertices if v.value == value), None)
