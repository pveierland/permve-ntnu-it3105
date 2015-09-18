import functols

class problem(object):

    @staticmethod
    def from_string(input):
        def parse_coordinate(input):
            return dict(zip(['x', 'y'], map(int, input.split(','))))

        def parse_rectangle(input):
            return dict(zip(["x", "y", "width", "height"],
                            map(int, input.split(','))))
        
        def build_obstacle_map(grid, obstacles):
            return [ any((obstacle['x'] <= x < obstacle['x'] + obstacle['width']) and
                         (obstacle['y'] <= y < obstacle['y'] + obstacle['height'])
                     for obstacle in obstacles)
                   for y in range(0, grid['y']) for x in range(0, grid['x']) ]
        
        parts = filter(None, re.split('[()]+\\s*[()]*', input))

        return {
            "grid":      parse_coordinate(parts[0]),
            "start":     parse_coordinate(parts[1]),
            "goal":      parse_coordinate(parts[2]),
            "obstacles": [ parse_rectangle(p) for p in parts[3:] ],
            "obstacle_map" : build_obstacle_map(parse_coordinate(
                parts[0]), [ parse_rectangle(p) for p in parts[3:] ])
        }
