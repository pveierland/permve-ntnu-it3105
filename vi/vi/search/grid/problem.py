import vi.grid

class Problem(object):
    @classmethod
    def from_grid_file(cls, filename):
        cell_values = {
            'w': 100, 'm': 50, 'f': 10, 'g': 5, 'r': 1, '.': 1, '#': -1
        }
    
        with open(filename, 'r') as f:
            map_data = [ line.strip() for line in f.readlines() if line.strip() ]
    
            grid = vi.grid.Grid(width = len(map_data[0]), height = len(map_data))
    
            start = None
            goal  = None
    
            # x, y is indexed with (0, 0) at bottom left of map:
            for y, line in enumerate(reversed(map_data)):
                for x, value in enumerate(line):
                    if value == 'A':
                        start = vi.grid.Coordinate(x, y)
                    elif value == 'B':
                        goal = vi.grid.Coordinate(x, y)
                    else:
                        grid.values[y][x] = cell_values[value]
    
            if not start:
                raise ValueError("{0}: no start location found".format(filename))
    
            if not goal:
                raise ValueError("{0}: no goal location found".format(filename))
    
            return cls(grid, start, goal)

    def __init__(self, grid, start, goal):
        self.grid  = grid
        self.start = start
        self.goal  = goal

    def actions(self, state):
        if not is_blocked(state.up()):
            yield Action.move_up
        if not is_blocked(state.down()):
            yield Action.move_down
        if not is_blocked(state.left()):
            yield Action.move_left
        if not is_blocked(state.right()):
            yield Action.move_right

    def goal_test(self, state):
        return self.state == self.goal

    def initial_state(self):
        return self.start
    
    def is_blocked(position):
        return position.x < 0 or \
               position.x >= self.grid.width or \
               position.y < 0 or \
               position.y >= self.grid.height or \
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
