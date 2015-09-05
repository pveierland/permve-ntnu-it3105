class graph_search_node(object):
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state     = state
        self.parent    = parent
        self.action    = action
        self.path_cost = path_cost
    
    def __eq__(self, other):
        return self.path_cost == other.path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def __str__(self):
        return 'graph_search_node(state={0},parent={1},action={2},path_cost={3})'.format(
            self.state, self.parent, self.action, self.path_cost)
