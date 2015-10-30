import vi.csp

import collections
import operator

BacktrackStatistics = collections.namedtuple(
    'BacktrackStatistics', ['calls', 'failures'])

def backtrack_search(network):
    statistics = BacktrackStatistics(calls=0, failures=0)
    # Ensure arc consistency before making any assumptions:
    return backtrack(vi.csp.general_arc_consistency(network), statistics)

def backtrack(network, statistics):
    def select_unassigned_variable():
        # Use Minimum-Remaining-Values heuristic:
        return min(((variable, domain)
                       for variable, domain in network.domains.items()
                       if len(domain) > 1),
                   key=operator.itemgetter(1))[0]

    def order_domain_variables():
        return network.domains[variable]

    statistics = BacktrackStatistics(statistics.calls + 1,
                                     statistics.failures)

    if all(len(domain) == 1 for domain in network.domains.values()):
        return network, statistics

    variable = select_unassigned_variable()

    for value in order_domain_variables():
        successor = network.copy()
        successor.domains[variable] = [value]
        successor = vi.csp.general_arc_consistency_rerun(successor, variable)

        if all(len(domain) >= 1
               for domain in successor.domains.values()):

            result, statistics = backtrack(successor, statistics)

            if result:
                return result, statistics

    statistics = BacktrackStatistics(statistics.calls,
                                     statistics.failures + 1)

    return None, statistics
