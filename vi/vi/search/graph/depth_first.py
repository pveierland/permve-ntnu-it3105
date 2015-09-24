from collections import deque

import vi.search.graph

def depth_first(problem):
    node = vi.search.graph.Node(problem.initial_state())

    if problem.goal_test(node.state):
        return vi.search.graph.Solution(node)

    # Search nodes on the 'open list' are stored in both a
    # list and a set. The list allows new nodes to be added
    # to the end and removed from the end in O(1) time;
    # while the set allows testing if a node is in the
    # 'open list' in O(1) time.
    # Search nodes in the 'closed list' are only stored in
    # a set since members are never removed from it.

    open_list  = [node]
    open_set   = set(node)
    closed_set = set()
    
    while open_list:
        # Get next node from the end of the 'open list':
        node = open_list.pop()
        open_set.remove(node)

        # Add current node to the 'closed list':
        closed_set.add(node)

        for action in problem.actions(node.state):
            child = vi.search.graph.child_node(problem, node, action)

            if child not in open_set and child not in closed_set:
                if problem.goal_test(child.state):
                    return vi.search.graph.Solution(child)

                # Add child node to the end of the 'open list':
                open_list.push(child)
                open_set.add(child)
