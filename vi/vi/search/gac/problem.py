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
        for variable, domain in node.state.domains.iteritems():
            for value in node.state.domains[variable]:
                new_state = node.state.copy()
                # Set singular domain for assumed variable:
                new_state.domains[variable] = [value]

                new_revised_state = vi.csp.general_arc_consistency(new_state)

                if self.__is_valid(new_revised_state):
                    yield Successor(
                        problem   = self,
                        parent    = node,
                        state     = new_revised_state,
                        action    = (variable, value),
                        step_cost = 1)

    def __is_valid(self, state):
        return all(len(domain) >= 1
                   for variable, domain in state.domains.iteritems())
