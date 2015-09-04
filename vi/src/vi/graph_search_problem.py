from graph_search_action import *
from graph_search_node import *

class graph_search_problem(object):
    def __init__(self, graph, start_vertex, goal_vertex):
        self.graph        = graph
        self.start_vertex = start_vertex
        self.goal_vertex  = goal_vertex

    def actions(self, state):
        for edge in state.edges:
            yield graph_search_action(state, edge)
    
    def build_child_node(self, parent_search_node, action):
        return graph_search_node(
            action.follow(parent_search_node.state),
            parent_search_node,
            action,
            parent_search_node.path_cost + action.edge.cost)
    
    def initial_state(self):
        return self.start_vertex

    def is_goal_state(self, state):
        return state == self.goal_vertex
