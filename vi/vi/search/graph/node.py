def child_node(problem, parent, action):
    state           = problem.result(parent.state, action)
    path_cost       = parent.path_cost + problem.step_cost(parent.state, action)
    heuristic_value = problem.heuristic(state) if hasattr(problem, 'heuristic') else 0
    return Node(state, parent, action, path_cost, heuristic_value)

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

    def add_child(self, child, action):
        self.children.append((child, action))
    
    def attach(self, parent, path_cost):
        self.parent    = parent
        self.path_cost = path_cost

    def propagate(self, problem):
        for child, action in self.children:
            new_path_cost = self.path_cost + problem.step_cost(self.state, action)

            if new_path_cost < child.path_cost:
                child.attach(self, new_path_cost)
                child.propagate()

    def total_cost_estimate(self):
        return self.path_cost + self.heuristic_value
