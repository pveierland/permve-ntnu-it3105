from graph_search_action import *
from graph_search_node import *
from graph_search_solution import *
from vertex import *

class graph_search_problem(object):
    def __init__(self, graph, start, goal):
        self.graph        = graph
        self.start_vertex = start if start is vertex else graph.lookup(start)
        self.goal         = goal

    def actions(self, state):
        for edge in state.edges:
            yield graph_search_action(state, edge)
    
    def build_child_node(self, parent_search_node, action):
        return graph_search_node(
            action.edge.follow(parent_search_node.state),
            parent_search_node,
            action,
            parent_search_node.path_cost + action.edge.cost)

    def build_solution(self, node):
        return graph_search_solution(node)

    def initial_state(self):
        return self.start_vertex

    def is_goal_state(self, state):
        if self.goal is vertex:
            return state == self.goal.state
        else:
            return state.value == self.goal
