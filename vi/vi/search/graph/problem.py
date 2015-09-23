import vi.graph
import vi.search.graph

class Problem(object):
    def __init__(self, graph, start, goal):
        self.graph        = graph
        self.start_vertex = start if start is vi.graph.Vertex else graph.lookup(start)
        self.goal         = goal

    def actions(self, state):
        for edge in state.edges:
            yield vi.search.graph.Action(state, edge)
    
    def build_child_node(self, parent_search_node, action):
        return vi.search.graph.Node(
            action.edge.follow(parent_search_node.state),
            parent_search_node,
            action,
            parent_search_node.path_cost + action.edge.cost)

    def build_node(self, state):
        return vi.search.graph.Node(state)

    def initial_state(self):
        return self.start_vertex

    def is_goal_state(self, state):
        if self.goal is vi.graph.Vertex:
            return state == self.goal.state
        else:
            return state.value == self.goal
