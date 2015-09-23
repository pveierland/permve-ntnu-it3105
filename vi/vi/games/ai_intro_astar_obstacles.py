import vi.grid

class AiIntroAstarObstacles(object):
    @staticmethod
    def map_type_to_value(type):
        if   type == '.': return  1
        elif type == '#': return -1
        else: raise ValueError("unknown map element type '{0}'".format(type))
    
    @staticmethod
    def map_value_to_type(value):
        if   value ==  1: return '.'
        elif value == -1: return '#'
        else: raise ValueError("unknown map element value '{0}'".format(value))

    @staticmethod
    def load_grid(filename):
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
                        grid.values[y][x] = AiIntroAstarObstacles.map_type_to_value(value)

            if not start:
                raise ValueError("{0}: no start location found".format(filename))

            if not goal:
                raise ValueError("{0}: no goal location found".format(filename))

            return grid

    def __init__(self, filename):
        grid = AiIntroAstarObstacles.load_grid(filename)
        print(grid)

