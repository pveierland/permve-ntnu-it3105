from collections import deque

import vi.search.graph

def breadth_first(problem):
    node = vi.search.graph.Node(problem.initial_state())

    if problem.goal_test(node.state):
        return vi.search.graph.Solution(node)
    
    # Search nodes on the 'open list' are stored in a deque.
    # This allows nodes to be removed from the front of the
    # 'open list' and added to the end of the 'open list'
    # in O(1) time.
    # States corresponding to the search nodes in the
    # 'open list' are kept in a set. This allows testing
    # if newly generated states already exist using a
    # lookup with O(1) cost. In the same manner a set is
    # used to keep states corresponding to nodes in the
    # 'closed list'. Since only the knowledge of which
    # states have been explored is needed, only the states
    # from the 'closed list' are kept stored and the
    # nodes on the 'closed list' are discarded.

    open_deque = deque([node])
    open_set   = set([node.state])
    closed_set = set()

    while open_deque:
        # Get node from the beginning of the 'open list':
        node = open_deque.popleft()
        open_set.remove(node.state)

        # Add current node to the 'closed list':
        closed_set.add(node.state)

        for action in problem.actions(node.state):
            child = vi.search.graph.child_node(problem, node, action)

            if child.state not in open_set and child.state not in closed_set:
                if problem.goal_test(child.state):
                    return vi.search.graph.Solution(child)

                # Add child node to end of the 'open list':
                open_deque.append(child)
                open_set.add(child.state)
