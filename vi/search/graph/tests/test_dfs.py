# -*- coding: utf-8 -*-

from nose.tools import *

import vi.graph
import vi.search.graph

def build_romania_graph():
    return vi.graph.graph([
        [ 'Sibiu',          'Rimnicu Vilcea', 80 ],
        [ 'Sibiu',          'Fagaras',        99 ],
        [ 'Fagaras',        'Bucharest',     211 ],
        [ 'Rimnicu Vilcea', 'Pitesti',        97 ],
        [ 'Pitesti',        'Bucharest',     101 ]])

def test_unconnected_vertex_not_found():
    graph = build_romania_graph()
    graph.insert_vertex('Oslo')
    problem = vi.search.graph.problem(graph, 'Sibiu', 'Oslo')
    assert not vi.search.graph.dfs(problem)

def test_find_solution():
    graph   = build_romania_graph()
    problem = vi.search.graph.problem(graph, 'Sibiu', 'Bucharest')
    result  = vi.search.graph.dfs(problem)
    assert result
