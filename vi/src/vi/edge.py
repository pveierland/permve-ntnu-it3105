# -*- coding: utf-8 -*-
class edge(object):
    def __init__(self, a, b, cost=1):
        self.a    = a
        self.b    = b
        self.cost = cost

    def __str__(self):
        return "{0} ← {1} → {2}".format(self.a, self.cost, self.b)

    def follow(self, vertex):
        return self.b if vertex is self.a else self.b
