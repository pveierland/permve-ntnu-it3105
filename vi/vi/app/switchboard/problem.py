import collections
import copy
import enum
import itertools
import numpy
import random

class Direction(enum.Enum):
    up    = 1
    down  = 2
    left  = 3
    right = 4

Point = collections.namedtuple('Point', ['x', 'y'])

class Problem(object):
    def __init__(self, M, N, D, W, start, end):
        self.M     = M
        self.N     = N
        self.D     = D
        self.W     = W
        self.start = start
        self.end   = end

    def evaluate(self, state):
        grid = numpy.zeros((self.N, self.M), dtype=bool)
        for p in range(1, len(state)):
            from_x = min(state[p-1].x, state[p].x)
            to_x   = max(state[p-1].x, state[p].x)
            from_y = min(state[p-1].y, state[p].y)
            to_y   = max(state[p-1].y, state[p].y)

            for y in range(from_y, to_y):
                for x in range(from_x, to_x):
                    grid[x, y] = True

        return grid.sum() / (self.M * self.N)

    def initial(self):
        if self.start.x == self.end.x or self.start.y == self.end.y:
            return [self.start, self.end]
        else:
            return [self.start, Point(self.start.x, self.end.y), self.end]

    def random_successor(self, state):
        def valid_horizontal_moves(a, b, x, y1, y2):
            return filter(\
                lambda x: (x[0] == a or x[0] == b or x[0] not in state) and \
                          (x[1] == a or x[1] == b or x[1] not in state),
                ((Point(new_x, y1), Point(new_x, y2)) \
                 for new_x in itertools.chain(
                     range(0, x), range(x + 1, self.N))))

        def valid_vertical_moves(a, b, y, x1, x2):
            return filter(\
                lambda x: (x[0] == a or x[0] == b or x[0] not in state) and \
                          (x[1] == a or x[1] == b or x[1] not in state),
                ((Point(first.x, new_y), Point(second.x, new_y)) \
                 for new_y in itertools.chain(
                     range(0, first.y), range(first.y + 1, self.M))))

        print('state={0}'.format(state))

        successor_state = copy.deepcopy(state)

        while True:
            if len(state) > 3 and random.choice([True, False]):
                # Move segment

                segment_index  = random.randrange(1, len(state) - 2)
                first, second  = state[segment_index], state[segment_index+1]
                previous_point = state[segment_index-1]
                next_point     = state[segment_index+2]

                print("first={0} second={1}".format(first, second))

                if first.x == second.x:
                    # Vertical segment

                    if first.y < second.y:
                        upper, lower = first, second
                    else:
                        lower, upper = first, second

                    random.sample(range(upper.y, lower.y), 2)

                    moves = list(valid_horizontal_moves(first, second))

                    valid_horizontal_moves(
                        previous_point, first.x, 
                elif first.y == second.y:
                    # Horizontal segment
                    moves = list(valid_vertical_moves(first.y, first.x, second.x))
                if moves:
                    first_on_line =

                    first.x == state[segment_index-1].x and first.x ==

                    successor_state[segment_index:segment_index+2] = random.choice(moves)

                    # Collapse
                    if successor_state[segment_index-1] == \
                       successor_state[segment_index]:
                        del successor_state[segment_index]
                        segment_index = segment_index - 1

                    if successor_state[segment_index+1] == \
                       successor_state[segment_index+2]:
                        del successor_state[segment_index+1]

                    # Successfully generated successor state
                    break
            else:
                # Split segment
                segment_index = random.randrange(len(state) - 1)

                first, second = state[segment_index], state[segment_index+1]

                if abs(first.x - second.x) > 1:
                    new_x = random.randrange(
                        min(first.x, second.x) + 1, max(first.x, second.x))
                    successor_state.insert(segment_index + 1, Point(new_x, first.y))
                    # Successfully generated successor state
                    break
                elif abs(first.y - second.y) > 1:
                    new_y = random.randrange(
                        min(first.y, second.y) + 1, max(first.y, second.y))
                    successor_state.insert(segment_index + 1, Point(first.x, new_y))
                    # Successfully generated successor state
                    break

        return successor_state
