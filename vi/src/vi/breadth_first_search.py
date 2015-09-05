from graph_search_node import *

def breadth_first_search(problem):
    node = graph_search_node(problem.initial_state())
    if problem.is_goal_state(node.state):
        print("IS GOAL STATE A")
        return problem.build_solution(node)
    frontier = [node]
    explored = set()
    while True:
        if not frontier:
            return None
        node = frontier.pop(0)
        print("EXAMINING NODE {0}".format(node))
        explored.add(node.state)
        for action in problem.actions(node.state):
            print("WORKING ON ACTION {0}".format(action))
            child = problem.build_child_node(node, action)
            if child.state not in explored or child.state not in frontier:
                if problem.is_goal_state(child.state):
                    print("IS GOAL STATE B")
                    return problem.build_solution(node)
                frontier.append(child)
