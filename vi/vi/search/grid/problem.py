import vi.grid

class problem(object):
    def __init__(self, grid, start, goal)
        self.grid  = grid
        self.start = start
        self.goal  = goal

    def actions(self, state):
        if not is_blocked(state.up()):
            yield vi.search.grid.action.action.move_up
        if not is_blocked(state.down()):
            yield vi.search.grid.action.action.move_down
        if not is_blocked(state.left()):
            yield vi.search.grid.action.action.move_left
        if not is_blocked(state.right()):
            yield vi.search.grid.action.action.move_right

    def goal_test(self, state):
        return state == goal

    def initial_state(self):
        return start
    
    def is_blocked(position):
        return position.x < 0 or
               position.x >= self.grid.width or
               position.y < 0 or
               position.y >= self.grid.height or
               self.grid.values[position.y][position.x] == vi.grid.obstructed
 
    def result(self, state, action):
        if action == vi.search.grid.action.move_up:
            return state.up()
        elif action == vi.search.grid.action.move_down:
            return state.down()
        elif action == vi.search.grid.action.move_left:
            return state.left()
        elif action == vi.search.grid.action.move_right:
            return state.right()

    def step_cost(self, state, action):
        return 1
