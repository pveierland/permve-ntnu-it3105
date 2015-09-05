from graph_search_action import *
from graph_search_node import *

class graph_search_problem(object):
    def __init__(self, graph, start_vertex, goal_vertex):
        self.graph        = graph
        self.start_vertex = start_vertex
        self.goal_vertex  = goal_vertex

    def actions(self, state):
        print("GETTING ACTIONS for {0} {1}".format(state, ', '.join(map(str, state.edges))))
        for edge in state.edges:
            print("EDGY {0}".format(edge))
            yield graph_search_action(state, edge)
    
    def build_child_node(self, parent_search_node, action):
        return graph_search_node(
            action.edge.follow(parent_search_node.state),
            parent_search_node,
            action,
            parent_search_node.path_cost + action.edge.cost)

    def build_solution(self, node):
        path = []
        while node:
            path.insert(0, node.state.value)
            node = node.parent
        return path

    def initial_state(self):
        return self.start_vertex

    def is_goal_state(self, state):
        return state == self.goal_vertex
