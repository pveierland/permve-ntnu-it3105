# -*- coding: utf-8 -*-

from edge import *
from vertex import *

class graph(object):
    def __init__(self, initial=None, edges=None):
        if not initial or initial[0] is vertex:
            self.vertices, self.edges = set(vertices), set(edges)
        else:
            self.vertices, self.edges = set(), set()
            for i in initial: self.link(*i)

    def __str__(self):
        return '\n'.join(str(e) for e in self.edges)
    
    def get_vertex(self, x):
        return x if x is vertex else self.lookup(x) or self.insert_vertex(x)

    def insert_vertex(self, x):
        v = x if x is vertex else vertex(x)
        self.vertices.add(v)
        return v
    
    def link(self, a, b, cost=None):
        v1 = self.get_vertex(a)
        v2 = self.get_vertex(b)
        e = edge(v1, v2, cost)
        self.edges.add(e)
        return e

    def lookup(self, value):
        return next((v for v in self.vertices if v.value == value), None)
