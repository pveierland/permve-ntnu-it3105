# -*- coding: utf-8 -*-
class vertex(object):
    def __init__(self, value, edges=set()):
        self.value = value
        self.edges = edges

    def __str__(self):
        return str(self.value)
