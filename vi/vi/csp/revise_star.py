import itertools

def revise_star(focal_variable, constraint, network):
    def domain_cross_product(focal_value):
        return (dict(zip(
            itertools.chain(non_focal_domains, {focal_variable: focal_value}), x))
            for x in itertools.product(
                *itertools.chain(non_focal_domains.values(), [[focal_value]])))

    variables = { variable
                  for variable in constraint.variables
                  if variable is not focal_variable }

    non_focal_domains = { variable: network.domains[variable]
                          for variable in variables }

    return [ value
             for value in network.domains[focal_variable]
             if any(constraint(values)
                    for values in domain_cross_product(value)) ]
