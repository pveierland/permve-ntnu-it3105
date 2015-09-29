from vi.search.graph import Node

class Successor(object):
    def __init__(self, problem, parent, state, action, step_cost):
        self.problem   = problem
        self.parent    = parent
        self.state     = state
        self.action    = action
        self.step_cost = step_cost

    def build_node(self):
        path_cost       = self.parent.path_cost + self.step_cost
        heuristic_value = self.problem.heuristic(self.state) \
                          if hasattr(self.problem, 'heuristic') \
                          else 0

        return Node(self.state,
                    self.parent,
                    self.action,
                    path_cost,
                    heuristic_value)
