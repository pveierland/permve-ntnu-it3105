# -*- coding: utf-8 -*-

class Edge(object):
    def __init__(self, a, b, cost=1):
        self.a    = a
        self.b    = b
        self.cost = cost

    def __str__(self):
        return "{0} ← {1} → {2}".format(self.a.value, self.cost, self.b.value)

    def build_str(self, from_vertex):
        return '{0} → {1}'.format(self.cost, self.follow(from_vertex).value)

    def follow(self, from_vertex):
        return self.b if from_vertex is self.a else self.a
