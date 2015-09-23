def dfs(problem):
    current_node = node(problem.initial_state())

    if problem.goal_test(current_node.state):
        return solution(current_node)

    frontier = [ current_node ]
    explored = set()

    while frontier:
        current_node = frontier.pop()
        explored.add(current_node.state)

        for action in problem.actions(current_node.state):
            child = child_node(problem, node, action)
            if child not in frontier and child.state not in explored:
                if problem.goal_test(child.state):
                    return problem.solution(child)
                frontier.append(child)
