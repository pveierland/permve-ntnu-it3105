class Node(object):
    def __init__(self, state, parent=None, action=None,
                 path_cost=0, heuristic_value=0):
        self.state           = state
        self.parent          = parent
        self.action          = action
        self.path_cost       = path_cost
        self.heuristic_value = heuristic_value
        self.children        = []

    def __lt__(self, other):
        return self.total_cost_estimate() < other.total_cost_estimate()

    def add_child(self, node, action, step_cost):
        self.children.append((node, action, step_cost))

    def attach(self, parent, path_cost):
        self.parent    = parent
        self.path_cost = path_cost

    def propagate(self, problem):
        for child, action, step_cost in self.children:
            new_path_cost = self.path_cost + step_cost

            if new_path_cost < child.path_cost:
                child.attach(self, new_path_cost)
                child.propagate()

    def total_cost_estimate(self):
        return self.path_cost + self.heuristic_value
