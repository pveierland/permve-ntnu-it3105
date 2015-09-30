import vi.app.astar_navigation

def test_parse_grid_problem():
    problem = vi.app.astar_navigation.parse_grid_problem(
        '6 7\n'
        '1 0 4 5\n'
        '3 2 2 2\n'
        '0 3 1 3\n'
        '2 0 4 2\n'
        '2 5 2 1\n')

    assert problem.grid.width  == 6
    assert problem.grid.height == 7
    assert problem.start.x     == 1
    assert problem.start.y     == 0
    assert problem.goal.x      == 4
    assert problem.goal.y      == 5

    assert problem.grid.values[0][0] ==  1
    assert problem.grid.values[0][2] == -1
    assert problem.grid.values[0][5] == -1
    assert problem.grid.values[2][2] ==  1
    assert problem.grid.values[5][2] == -1
