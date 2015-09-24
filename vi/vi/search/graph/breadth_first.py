from collections import deque

import vi.search.graph

def breadth_first(problem):
    node = vi.search.graph.Node(problem.initial_state())

    if problem.goal_test(node.state):
        return vi.search.graph.Solution(node)

    # Search nodes on the 'open list' are stored in both a
    # deque and a set. The deque allows new nodes to be
    # added to the end and removed from the front in O(1)
    # time; while the set allows testing if a node is in
    # the 'open list' in O(1) time. Search nodes in the
    # 'closed list' are only stored in a set since members
    # are never removed from it.

    open_deque = deque(node)
    open_set   = set(node)
    closed_set = set()

    while open_deque:
        # Get node from the beginning of the 'open list':
        node = open_deque.popleft()
        open_set.remove(node.state)

        # Add current node to the 'closed list':
        closed_set.add(node.state)

        for action in problem.actions(node.state):
            child = vi.search.graph.child_node(problem, node, action)

            if child not in open_set and child not in closed_set:
                if problem.goal_test(child.state):
                    return vi.search.graph.Solution(child)

                # Add child node to end of the 'open list':
                open_deque.append(child)
                open_set.add(child.state)
