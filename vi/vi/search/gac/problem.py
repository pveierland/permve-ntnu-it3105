import vi.csp
from vi.search.graph import Node, Successor

class Problem(object):
    def __init__(self, start):
        self.start = start

    def goal_test(self, state):
        return all(len(domain) == 1
                   for variable, domain in state.domains.iteritems())

    def heuristic(self, state):
        return sum(len(domain) - 1
                   for variable, domain in state.domains.iteritems())

    def initial_node(self):
        return Node(vi.csp.general_arc_consistency(self.start))

    def successors(self, node):
        def get_assumption_variable():
            variable, domain = min(((v, d) \
                for v, d in node.state.domains.iteritems()
                if len(d) != 1), key=lambda x: len(x[1]))
            return variable

        variable = get_assumption_variable()

        for value in node.state.domains[variable]:
            successor_state = node.state.copy()
            successor_state.domains[variable] = [value]
            successor_state = vi.csp.general_arc_consistency_rerun(
                successor_state, variable)

            if self.__is_valid(successor_state):
                yield Successor(
                    problem   = self,
                    parent    = node,
                    state     = successor_state,
                    action    = (variable, value),
                    step_cost = 1)

    def __is_valid(self, state):
        return all(len(domain) >= 1
                   for variable, domain in state.domains.iteritems())
