import vi.grid

def map_type_to_value(type):
    if   type == 'w': return 100
    elif type == 'm': return 50
    elif type == 'f': return 10
    elif type == 'g': return 5
    elif type == 'r': return 1
    else:             return -1

def map_value_to_type(value):
    if   value == 100: return 'w'
    elif value ==  50: return 'm'
    elif value ==  10: return 'f'
    elif value ==   5: return 'g'
    elif value ==   1: return 'r'
    elif value ==  -1: return '#'
    else:              return '?'

class ai_intro_astar(object):
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
                        grid.values[y][x] = map_type_to_value(value)

            if not start:
                raise ValueError("{0}: no start location found".format(filename))

            if not goal:
                raise ValueError("{0}: no goal location found".format(filename))

            print("start = {0} goal = {1}".format(start, goal))
            print(grid)

