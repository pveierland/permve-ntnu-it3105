import enum

recursive_depth_limited_search_result = enum.Enum(
    'recursive_depth_limited_search_result',
    'cutoff failure')

def recursive_depth_limited_search(node, problem, limit):
    if problem.is_goal_state(node):
        return problem.get_solution(node)
    elif limit == 0:
        return recursive_depth_limited_search_result.cutoff
    return recursive_depth_limited_search.failure
