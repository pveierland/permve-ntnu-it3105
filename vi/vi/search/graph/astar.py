import heapq

import vi.search.graph

def astar(problem):
    node = vi.search.graph.Node(problem.initial_state())

    # Search nodes on the 'open list' are both stored in a
    # heap queue and a hash table. The heap queue keeps
    # search nodes sorted by their total estimated path cost
    # and allows nodes to be added and removed from the
    # queue in O(1) time. The hash table used for the
    # 'open list' and 'closed list' makes it possible
    # to retrieve a node from a given state in O(1) time.
    open_heap_queue   = [node]
    open_hash_table   = {node.state: node}
    closed_hash_table = {}

    while open_heap_queue:
        # Retrieve current node from 'open list':
        node = heapq.heappop(open_heap_queue)
        del open_hash_table[node.state]

        # Add current node to 'closed list':
        closed_hash_table[node.state] = node

        if problem.goal_test(node.state):
            return vi.search.graph.Solution(node)

        for action in problem.actions(node.state):
            successor_state = problem.result(node.state, action)

            open_entry = open_hash_table.get(successor_state)
            closed_entry = None if open_entry else \
                closed_hash_table.get(successor_state)

            if not open_entry and not closed_entry:
                successor_node = vi.search.graph.child_node(
                    problem, node, action)

                # Add successor node to 'open list':
                heapq.heappush(open_heap_queue, successor_node)
                open_hash_table[successor_state] = successor_node
            else:
                successor_node = open_entry or closed_entry
                successor_path_cost = node.path_cost + \
                    problem.step_cost(node.state, action)

                if successor_path_cost < successor_node.path_cost:
                    successor_node.attach(node, successor_path_cost)

                    if closed_entry:
                        successor_node.propagate(problem)

                    # Node costs in open list may have changed:
                    heapq.heapify(open_heap_queue)
            
            node.add_child(successor_node, action)
