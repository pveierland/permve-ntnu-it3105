from graph_search_node import *
from graph_search_problem import *
from graph_search_solution import *

def breadth_first_search(*args):
    problem = args[0] if args[0] is graph_search_problem else graph_search_problem(*args)

    node = graph_search_node(problem.initial_state())

    if problem.is_goal_state(node.state):
        return graph_search_solution(node)

    frontier = [ node ]
    explored = set()

    while frontier:
        node = frontier.pop(0)
        explored.add(node.state)

        for action in problem.actions(node.state):
            child = problem.build_child_node(node, action)
            if child not in frontier and child.state not in explored:
                if problem.is_goal_state(child.state):
                    return graph_search_solution(child)
                frontier.append(child)
