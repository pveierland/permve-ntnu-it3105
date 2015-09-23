import vi.graph
import vi.search.graph

def BreadthFirstSearch(problem):
    node = vi.search.graph.Node(problem.initial_state())

    if problem.goal_test(node.state):
        return vi.search.graph.Solution(node)

    frontier = [ node ]
    explored = set()

    while frontier:
        node = frontier.pop(0)
        explored.add(node.state)

        for action in problem.actions(node.state):
            child = vi.search.graph.child_node(problem, node, action)

            if child not in frontier and child.state not in explored:
                if problem.goal_test(child.state):
                    return vi.search.graph.Solution(child)

                frontier.append(child)
