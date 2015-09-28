def revise_star(focal_variable, state):
    def domain_cross_product(domains):
        return (dict(izip(domains, x)) for x in product(*domains.itervalues()))

    relevant_variables = {
        variable for constraint in focal_variable.constraints
                 for variable in constraint.variables }

    domains = { variable: state.domains[variable]
                for variable in relevant_variables }

    return [ values[focal_variable]
             for values in domain_coss_product(domains)
                 if all(contraint(values)
                        for constraint in focal_variable.constraints) ]
