import vi.grid

class ai_intro_astar_obstacles(object):
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

    def __init__(self, filename):
        with open(filename, 'r') as f:
            map_description = [ line.strip() for line in f.readlines() if line.strip() ]

            map_width  = len(map_description[0])
            map_height = len(map_description)
            
            grid = vi.grid.grid(map_width, map_height)

            start = None
            goal  = None

            # x, y is indexed with (0, 0) at bottom left of map:
            for y, line in enumerate(reversed(map_description)):
                for x, value in enumerate(line):
                    if value == 'A':
                        start = vi.grid.coordinate(x, y)
                    elif value == 'B':
                        goal = vi.grid.coordinate(x, y)
                    else:
                        grid.values[y][x] = self.map_type_to_value(value)

            if not start:
                raise ValueError("{0}: no start location found".format(filename))

            if not goal:
                raise ValueError("{0}: no goal location found".format(filename))

            print("start = {0} goal = {1}".format(start, goal))
            print(grid)

