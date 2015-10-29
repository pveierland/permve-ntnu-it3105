import vi.csp

import collections

BacktrackStatistics = collections.namedtuple(
    'BacktrackStatistics', ['call_count', 'backtrack_count'])

def backtrack_search(network):
    # Ensure arc consistency before making any assumptions:
    statistics = BacktrackStatistics(call_count=0, backtrack_count=0)
    return backtrack(vi.csp.general_arc_consistency(network), statistics)

def backtrack(network, statistics):
    def select_unassigned_variable():
        # Use Minimum-Remaining-Values heuristic:
        #return min((domain, variable) for variable, domain in network.domains.items())[1]
        for variable, domain in network.domains.items():
            if len(domain) != 1:
                return variable

    def order_domain_variables():
        return network.domains[variable]

    statistics = BacktrackStatistics(statistics.call_count + 1,
                                     statistics.backtrack_count)

    if all(len(domain) == 1 for domain in network.domains.values()):
        return network, statistics

    variable = select_unassigned_variable()

    for value in order_domain_variables():#variable, assignment, network):
        successor = network.copy()
        successor.domains[variable] = [value]
        successor = vi.csp.general_arc_consistency_rerun(successor, variable)

        if all(len(domain) >= 1
               for domain in successor.domains.values()):

            result = backtrack(successor)

            if result:
                return result, statistics

    statistics.backtrack_count = BacktrackStatistics(statistics.call_count,
                                                     statistics.backtrack_count + 1)

    return None, statistics
