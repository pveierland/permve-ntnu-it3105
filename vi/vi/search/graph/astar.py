import heapq

import vi.search.graph

class AStar(object):
    def __init__(self, problem):
        self.problem = problem

    def search(self):
        node = vi.search.graph.Node(self.problem.initial_state())

        # Search nodes on the 'open list' are both stored in a
        # heap queue and a hash table. The heap queue keeps
        # search nodes sorted by their total estimated path cost
        # and allows nodes to be added and removed from the
        # queue in O(1) time. The hash table used for the
        # 'open list' and 'closed list' makes it possible
        # to retrieve a node from a given state in O(1) time.
        self.open_heap_queue   = [node]
        self.open_hash_table   = {node.state: node}
        self.closed_hash_table = {}

        while self.open_heap_queue:
            # Retrieve current node from 'open list':
            node = heapq.heappop(self.open_heap_queue)
            del self.open_hash_table[node.state]

            # Add current node to 'closed list':
            self.closed_hash_table[node.state] = node

            if self.problem.goal_test(node.state):
                return vi.search.graph.Solution(node)

            for action in self.problem.actions(node.state):
                successor_state = self.problem.result(node.state, action)

                open_entry = self.open_hash_table.get(successor_state)
                closed_entry = None if open_entry else \
                    self.closed_hash_table.get(successor_state)

                if not open_entry and not closed_entry:
                    successor_node = vi.search.graph.child_node(
                        self.problem, node, action)

                    # Add successor node to 'open list':
                    heapq.heappush(self.open_heap_queue, successor_node)
                    self.open_hash_table[successor_state] = successor_node
                else:
                    successor_node = open_entry or closed_entry
                    successor_path_cost = node.path_cost + \
                        self.problem.step_cost(node.state, action)

                    if successor_path_cost < successor_node.path_cost:
                        successor_node.attach(node, successor_path_cost)

                        if closed_entry:
                            successor_node.propagate(self.problem)

                        # Node costs in open list may have changed:
                        heapq.heapify(self.open_heap_queue)

                node.add_child(successor_node, action)
