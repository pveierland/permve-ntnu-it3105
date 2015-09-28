import vi.csp

def test_general_arc_consistency():
    w = vi.csp.Variable('W')
    x = vi.csp.Variable('X')
    y = vi.csp.Variable('Y')
    z = vi.csp.Variable('Z')

    constraint = vi.csp.Constraint(
        {w, x, y, z},
        (lambda v: v[w] + v[x] + v[y] < v[z] + 1))

    w.constraints = [constraint]
    x.constraints = [constraint]
    y.constraints = [constraint]
    z.constraints = [constraint]

    domains = { w: [1, 2, 3, 4, 5],
                x: [1, 2, 3, 4, 5],
                y: [1, 2, 3, 4, 5],
                z: [1, 2, 3, 4, 5] }

    network         = vi.csp.Network({w, x, y, z}, domains)
    revised_network = vi.csp.general_arc_consistency(network)

    assert revised_network.domains[w] == [1, 2, 3]
    assert revised_network.domains[x] == [1, 2, 3]
    assert revised_network.domains[y] == [1, 2, 3]
    assert revised_network.domains[z] == [3, 4, 5]
