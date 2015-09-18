def dfs(problem):
    node = problem.build_node(problem.initial_state())

    if problem.is_goal_state(node.state):
        return problem.solution(node)

    frontier = [ node ]
    explored = set()

    while frontier:
        node = frontier.pop()
        explored.add(node.state)

        for action in problem.actions(node.state):
            child = problem.build_child_node(node, action)
            if child not in frontier and child.state not in explored:
                if problem.is_goal_state(child.state):
                    return problem.solution(child)
                frontier.append(child)
