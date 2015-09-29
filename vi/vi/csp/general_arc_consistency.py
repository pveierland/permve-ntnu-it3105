import collections

import vi.csp

def general_arc_consistency(network):
    queue = collections.deque(
        (variable, constraint)
        for variable in network.variables
        for constraint in variable.constraints)

    while queue:
        variable, constraint = queue.popleft()
        
#        print("FIX CONSISTENCY {0} RELATING TO {1}".format(variable.identity.value, ','.join(str(v.identity.value) for v in constraint.variables if v != variable)))
#        
#        print("DOMAINS = {0}".format(
#                        '\n'.join('{0}:{1}'.format(str(var.identity.value), dom) for (var, dom) in network.domains.iteritems())))

        revised_domain = vi.csp.revise_star(
            variable, constraint, network)

        if len(revised_domain) != len(network.domains[variable]):
            network.domains[variable] = revised_domain

#            print("REVISED DOMAIN = {0}".format(revised_domain))

            queue.extend((v, c)
                         for c in variable.constraints
                         for v in c.variables
                         if c != constraint and v != variable)

    return network
