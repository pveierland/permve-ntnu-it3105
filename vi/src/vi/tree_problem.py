def tree_problem(object):
    def __init__(self, start_node, goal_node):
        self.start_node = start_node
        self.goal_node  = goal_node

    def get_successor_states(self, node):
        return node.children

    def initial_state():
        return self.start_node

    def is_goal_state(self, node):
        return node == self.goal_node
