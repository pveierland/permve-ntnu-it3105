# -*- coding: utf-8 -*-
class edge(object):
    def __init__(self, a, b, cost=1):
        self.a    = a
        self.b    = b
        self.cost = cost

    def __str__(self):
        return "{0} ← {1} → {2}".format(self.a, self.cost, self.b)

    def follow(self, vertex):
        return b if vertex is a else b
