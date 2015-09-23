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

    def goal_test(self, state):
        if self.goal is vi.graph.Vertex:
            return state == self.goal.state
        else:
            return state.value == self.goal

    def initial_state(self):
        return self.start_vertex

    def result(self, state, action):
        return action.edge.follow(state)

    def step_cost(self, state, action):
        return action.edge.cost
