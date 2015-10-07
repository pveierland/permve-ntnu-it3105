class Rectangle(object):
    def __init__(self, x, y, width, height):
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height

    def __eq__(self, other):
        return self.x == other.x and \
               self.y == other.y and \
               self.width == other.width and \
               self.height == other.height

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))

    def __str__(self):
        return "Rectangle(x={0},y={1},width={2},height={3})" \
            .format(self.x, self.y, self.width, self.height)

    def distance_to_coordinate(self, coordinate):
        end_x = self.coordinate.x + self.width - 1
        end_y = self.coordinate.y + self.height - 1

        if coordinate.x < self.x:
            diff_x = self.x - coordinate.x
        elif coordinate.x > end_x:
            diff_x = coordinate.x - end_x
        else:
            diff_x = 0

        if coordinate.y < self.y:
            diff_y = self.y - coordinate.y
        elif coordinate.y > end_y:
            diff_y = coordinate.y - end_y
        else:
            diff_y = 0

        return (diff_x, diff_y)

    def intersects_coordinate(self, coordinate):
        return (self.x <= coordinate.x) and \
               (coordinate.x < self.x + self.width) and \
               (self.y <= coordinate.y) and \
               (coordinate.y < self.y + self.height)
