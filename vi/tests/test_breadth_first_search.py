# -*- coding: utf-8 -*-

from nose.tools import *
import vi

def build_romania_graph():
    return vi.graph([
        [ 'Sibiu',          'Rimnicu Vilcea', 80 ],
        [ 'Sibiu',          'Fagaras',        99 ],
        [ 'Fagaras',        'Bucharest',     211 ],
        [ 'Rimnicu Vilcea', 'Pitesti',        97 ],
        [ 'Pitesti',        'Bucharest',     101 ]])

def test_unconnected_vertex_not_found():
    graph = build_romania_graph()
    graph.insert_vertex('Oslo')
    assert not vi.breadth_first_search(graph, 'Sibiu', 'Oslo')

def test_find_shallowest_solution():
    graph  = build_romania_graph()
    result = vi.breadth_first_search(graph, 'Sibiu', 'Bucharest')
    assert_equal(result.path, [ 'Sibiu', 'Fagaras', 'Bucharest' ])
    assert_equal(result.cost, 310)
