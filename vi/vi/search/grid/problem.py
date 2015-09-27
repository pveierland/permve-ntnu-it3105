import vi.grid
import vi.search.grid

class Problem(object):
    def __init__(self, grid, start, goal):
        self.grid  = grid
        self.start = start
        self.goal  = goal

    def actions(self, state):
        if not self.is_blocked(state.up()):
            yield vi.search.grid.Action.move_up
        if not self.is_blocked(state.down()):
            yield vi.search.grid.Action.move_down
        if not self.is_blocked(state.left()):
            yield vi.search.grid.Action.move_left
        if not self.is_blocked(state.right()):
            yield vi.search.grid.Action.move_right

    def goal_test(self, state):
        return state == self.goal

    def heuristic(self, state):
        # Use Manhattan heuristic:
        return abs(self.goal.x - state.x) + abs(self.goal.y - state.y)

    def initial_state(self):
        return self.start

    def is_blocked(self, position):
        return position.x < 0 or \
               position.x >= self.grid.width or \
               position.y < 0 or \
               position.y >= self.grid.height or \
               self.grid.values[position.y][position.x] == vi.grid.obstructed

    def result(self, state, action):
        if action == vi.search.grid.Action.move_up:
            return state.up()
        elif action == vi.search.grid.Action.move_down:
            return state.down()
        elif action == vi.search.grid.Action.move_left:
            return state.left()
        elif action == vi.search.grid.Action.move_right:
            return state.right()

    def step_cost(self, state, action):
        return 1
