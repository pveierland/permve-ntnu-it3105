from vi.grid import Coordinate, Grid, obstructed, Rectangle
from vi.search.grid import Problem

def parse_grid_problem(text):
    def parse_coordinate(text):
        return Coordinate(*map(int, text.strip().split()))

    def parse_rectangle(text):
        return Rectangle(*map(int, text.strip().split()))

    def parse_start_goal(text):
        parts = text.strip().split()
        return (Coordinate(int(parts[0]), int(parts[1])),
                Coordinate(int(parts[2]), int(parts[3])))

    lines = text.splitlines()

    dimensions = parse_coordinate(lines[0])
    start, goal = parse_start_goal(lines[1])
    obstacles = [parse_rectangle(l) for l in lines[2:]]

    grid = Grid(width=dimensions.x, height=dimensions.y)

    for obstacle in obstacles:
        for y in range(obstacle.y, obstacle.y + obstacle.height):
            for x in range(obstacle.x, obstacle.x + obstacle.width):
                grid.values[y][x] = obstructed

    return Problem(grid, start, goal)
