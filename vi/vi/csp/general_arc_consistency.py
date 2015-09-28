import collections

import vi.csp

def general_arc_consistency(network):
    revised_network = network.shallow_copy()

    queue = collections.deque(
        (variable, constraint)
        for variable in revised_network.variables
        for constraint in variable.constraints)

    while queue:
        variable, constraint = queue.popleft()

        revised_domain = vi.csp.revise_star(
            variable, constraint, revised_network)

        if len(revised_domain) != len(revised_network.domains[variable]):
            revised_network.domains[variable] = revised_domain

            queue.extend((v, c)
                         for c in variable.constraints
                         for v in c.variables
                         if c != constraint and v != variable)

    return revised_network
