import vi.grid

from vi.search.graph import Node, Successor
from vi.search.grid import Action

class Problem(object):
    def __init__(self, grid, start, goal):
        self.grid  = grid
        self.start = start
        self.goal  = goal

    def goal_test(self, state):
        return state == self.goal

    def heuristic(self, state):
        # Use Manhattan heuristic:
        return abs(self.goal.x - state.x) + abs(self.goal.y - state.y)

    def initial_node(self):
        return Node(self.start)

    def is_blocked(self, position):
        return position.x < 0 or \
               position.x >= self.grid.width or \
               position.y < 0 or \
               position.y >= self.grid.height or \
               self.grid.values[position.y][position.x] == vi.grid.obstructed

    def successors(self, node):
        for action in Action:
            if action == Action.move_up:
                successor_state = node.state.up()
            elif action == Action.move_down:
                successor_state = node.state.down()
            elif action == Action.move_left:
                successor_state = node.state.left()
            elif action == Action.move_right:
                successor_state = node.state.right()

            if not self.is_blocked(successor_state):
                yield Successor(self, node, successor_state, action, 1)
