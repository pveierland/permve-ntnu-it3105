import heapq

import vi.search.graph

class AStar(object):
    def __init__(self, problem):
        self.problem = problem

        initial_node = vi.search.graph.Node(self.problem.initial_state())

        # Search nodes on the 'open list' are both stored in a
        # heap queue and a hash table. The heap queue keeps
        # search nodes sorted by their total estimated path cost
        # and allows nodes to be added and removed from the
        # queue in O(1) time. The hash table used for the
        # 'open list' and 'closed list' makes it possible
        # to retrieve a node from a given state in O(1) time.
        self.open_heap_queue   = [initial_node]
        self.open_hash_table   = {initial_node.state: initial_node}
        self.closed_hash_table = {}

        self.state = (vi.search.graph.State.start, initial_node)

    def closed_list(self):
        return self.closed_hash_table.itervalues()

    def generate_node(self, action):
        successor_state = self.problem.result(self.node.state, action)

        open_entry = self.open_hash_table.get(successor_state)
        closed_entry = None if open_entry else \
            self.closed_hash_table.get(successor_state)

        if not open_entry and not closed_entry:
            is_successor_state_unique = True

            successor_node = vi.search.graph.child_node(
                self.problem, self.node, action)

            # Add successor node to 'open list':
            heapq.heappush(self.open_heap_queue, successor_node)
            self.open_hash_table[successor_state] = successor_node
        else:
            is_successor_state_unique = False

            successor_node = open_entry or closed_entry
            successor_path_cost = self.node.path_cost + \
                self.problem.step_cost(self.node.state, action)

            if successor_path_cost < successor_node.path_cost:
                successor_node.attach(self.node, successor_path_cost)

                if closed_entry:
                    successor_node.propagate(self.problem)

                # Values for nodes in 'open list' may have changed:
                heapq.heapify(self.open_heap_queue)

        self.node.add_child(successor_node, action)

        return (successor_node, is_successor_state_unique)

    def is_complete(self):
        return self.state[0] == vi.search.graph.State.failed or \
               self.state[0] == vi.search.graph.State.success

    def open_list(self):
        return self.open_heap_queue

    def step(self):
        if self.state[0] == vi.search.graph.State.start or \
           self.state[0] == vi.search.graph.State.expand_node_complete:

            if not self.open_heap_queue:
                self.state = (vi.search.graph.State.failed,)
                return self.state

            # Retrieve current node from 'open list':
            self.node = heapq.heappop(self.open_heap_queue)
            del self.open_hash_table[self.node.state]

            # Add current node to 'closed list':
            self.closed_hash_table[self.node.state] = self.node

            if self.problem.goal_test(self.node.state):
                solution = vi.search.graph.Solution(self.node)
                self.state = (vi.search.graph.State.success, self.node, solution)
                return self.state

            self.state = (vi.search.graph.State.expand_node_begin, self.node)
            return self.state

        if self.state[0] == vi.search.graph.State.expand_node_begin:
            self.actions = self.problem.actions(self.node.state)

        action = next(self.actions, None)

        if action:
            successor_node, is_successor_state_unique = self.generate_node(action)
            self.state = (vi.search.graph.State.generate_nodes,
                          self.node,
                          successor_node,
                          is_successor_state_unique)
        else:
            self.state = (vi.search.graph.State.expand_node_complete, self.node)

        return self.state
