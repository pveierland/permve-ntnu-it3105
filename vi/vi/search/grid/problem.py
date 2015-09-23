import vi.grid
import functols

class problem(object):
    @staticmethod
    def from_string_map_format(input):
        def cost_from_cell_type(type):
            if type == 'w': return 100
            elif type == 'm': return 50
            elif type == 'f': return 10

        self.width  = len(input[0])
        self.height = len(input)

        
        for line in input

        self.grid_size = vi.grid.coordinate(len(input)


    @staticmethod
    def from_string_1(input)
        def from_string(input):
        parts = filter(None, re.split('[()]+\\s*[()]*', input))
        
        return problem(
            grid_size = vi.grid.coordinate.from_string(parts[0]),
            start     = vi.grid.coordinate.from_string(parts[1]),
            goal      = vi.grid.coordinate.from_string(parts[2]),
            obstacles = [ vi.grid.xywh.from_string(p) for p in parts[3:] ])

    def __init__(self):
        def build_obstacle_map(grid, obstacles):
            return [ any((obstacle.x <= x < obstacle.x + obstacle.w) and
                         (obstacle.y <= y < obstacle.y + obstacle.h)
                     for obstacle in obstacles)
                   for y in range(0, grid.h) for x in range(0, grid.w) ]

        self.grid_size    = grid_size
        self.start        = start
        self.goal         = goal
        self.obstacles    = obstacles
        self.obstacle_map = build_obstacle_map(grid.width

                position
                dimension

                grid.width height 

        return {
            "grid":      parse_coordinate(parts[0]),
            "start":     parse_coordinate(parts[1]),
            "goal":      parse_coordinate(parts[2]),
            "obstacles": [ parse_rectangle(p) for p in parts[3:] ],
            "obstacle_map" : build_obstacle_map(parse_coordinate(
                parts[0]), [ parse_rectangle(p) for p in parts[3:] ])
        }



    "def parse_navigation_task(input):\n",
    "    def parse_coordinate(input):\n",
    "        return dict(zip(['x', 'y'], map(int, input.split(','))))\n",
    "\n",
    "    def parse_rectangle(input):\n",
    "        return dict(zip([\"x\", \"y\", \"width\", \"height\"], map(int, input.split(','))))\n",
    "    \n",
    "    def build_obstacle_map(grid, obstacles):\n",
    "        return [ any((obstacle['x'] <= x < obstacle['x'] + obstacle['width']) and\n",
    "                     (obstacle['y'] <= y < obstacle['y'] + obstacle['height'])\n",
    "                 for obstacle in obstacles)\n",
    "               for y in range(0, grid['y']) for x in range(0, grid['x']) ]\n",
    "    \n",
    "    parts = filter(None, re.split('[()]+\\s*[()]*', input))\n",
    "    \n",
    "    return {\n",
    "        \"grid\":      parse_coordinate(parts[0]),\n",
    "        \"start\":     parse_coordinate(parts[1]),\n",
    "        \"goal\":      parse_coordinate(parts[2]),\n",
    "        \"obstacles\": [ parse_rectangle(p) for p in parts[3:] ],\n",
    "        \"obstacle_map\" : build_obstacle_map(parse_coordinate(parts[0]), [ parse_rectangle(p) for p in parts[3:] ])\n",
    "    }\n",
