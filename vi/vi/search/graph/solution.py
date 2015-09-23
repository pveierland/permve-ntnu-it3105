class Solution(object):
    def __init__(self, node):
        self.cost = node.path_cost
        self.path = []

        while node:
            self.path.insert(0, node.state.value)
            node = node.parent
