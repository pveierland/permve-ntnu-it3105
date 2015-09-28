import itertools

def revise_star(focal_variable, state):
    def domain_cross_product(focal_value):
        return (dict(itertools.izip(
            itertools.chain(non_focal_domains, {focal_variable: focal_value}), x))
            for x in itertools.product(
                *itertools.chain(non_focal_domains.itervalues(), [[focal_value]])))

    variables = { variable
                  for constraint in focal_variable.constraints
                  for variable in constraint.variables
                  if variable is not focal_variable }

    non_focal_domains = { variable: state.domains[variable]
                          for variable in variables }

    return [ value
             for value in state.domains[focal_variable]
             if any(all(constraint(values)
                        for constraint in focal_variable.constraints)
                    for values in domain_cross_product(value)) ]
