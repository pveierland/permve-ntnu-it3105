import numpy
import random

class Problem(object):
    def __init__(self, M, N, K):
        self.M = M
        self.N = N
        self.K = K

        self.__upper_boundary = min(M, N) * K

    def evaluate(self, state):
        for row in range(self.M):
            if state[row,:].sum() > self.K:
                return -1

        for column in range(self.N):
            if state[:,column].sum() > self.K:
                return -1

        for d_i in range(-(self.M - self.K - 1), self.N - self.K):
            if numpy.trace(state, d_i) > self.K:
                return -1

            if numpy.fliplr(state).trace(d_i) > self.K:
                return -1

        return state.sum() / self.__upper_boundary

    def initial(self):
        return numpy.zeros((self.M, self.N), dtype=bool)

    def is_terminal(self, state):
        # Known optimal solution
        return state.sum() == self.__upper_boundary

    def random_successor(self, state):
        successor_state = numpy.copy(state)
        m = random.randrange(self.M)
        n = random.randrange(self.N)
        successor_state[m, n] = not successor_state[m, n]
        return successor_state
