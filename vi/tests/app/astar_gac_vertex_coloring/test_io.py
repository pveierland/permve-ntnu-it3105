import vi.app.astar_gac_vertex_coloring

def test_parse_graph_file_1():
    graph = vi.app.astar_gac_vertex_coloring.parse_graph_file((
        '3 3\n'
        '0 2.5 1.5\n'
        '1 4.0 4.0\n'
        '2 5.5 1.5\n'
        '0 1\n'
        '0 2\n'
        '1 2\n').split('\n'))

    vertex_0 = graph.lookup(lambda v: v.value[0] == 0)
    assert vertex_0.value[1][0] == 2.5
    assert vertex_0.value[1][1] == 1.5

    vertex_1 = graph.lookup(lambda v: v.value[0] == 1)
    assert vertex_1.value[1][0] == 4.0
    assert vertex_1.value[1][1] == 4.0

    vertex_2 = graph.lookup(lambda v: v.value[0] == 2)
    assert vertex_2.value[1][0] == 5.5
    assert vertex_2.value[1][1] == 1.5

    assert vertex_0.is_linked(vertex_1)
    assert vertex_0.is_linked(vertex_2)

    assert vertex_1.is_linked(vertex_0)
    assert vertex_1.is_linked(vertex_2)

    assert vertex_2.is_linked(vertex_0)
    assert vertex_2.is_linked(vertex_1)

