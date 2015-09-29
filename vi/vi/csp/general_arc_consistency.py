import collections

import vi.csp

def general_arc_consistency(network, queue=None):
    if not queue:
        queue = collections.deque(
            (variable, constraint)
            for variable in network.variables
            for constraint in variable.constraints)

    while queue:
        variable, constraint = queue.popleft()

        revised_domain = vi.csp.revise_star(
            variable, constraint, network)

        if len(revised_domain) != len(network.domains[variable]):
            network.domains[variable] = revised_domain

            queue.extend((v, c)
                         for c in variable.constraints
                         for v in c.variables
                         if c != constraint and v != variable)

    return network

def general_arc_consistency_rerun(network, variable):
    queue = collections.deque(
        (v, c)
        for c in variable.constraints
        for v in c.variables
        if v != variable)

    return general_arc_consistency(network, queue)
