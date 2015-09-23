def child_node(problem, parent, action):
    return Node(
        state     = problem.result(parent.state, action),
        parent    = parent,
        action    = action,
        path_cost = parent.path_cost + problem.step_cost(parent.state, action))

class Node(object):
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state     = state
        self.parent    = parent
        self.action    = action
        self.path_cost = path_cost
    
    def __eq__(self, other):
        return self.state == other.state if other is Node else self.state == other

    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def __str__(self):
        return 'node(state={0},parent={1},action={2},path_cost={3})'.format(
            self.state, self.parent, self.action, self.path_cost)
