import heapq

from vi.search.graph import Solution, State

class AStar(object):
    def __init__(self, problem):
        self.problem = problem

        initial_node = self.problem.initial_node()

        if initial_node:
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

            self.state, self.info = State.start, (initial_node,)
        else:
            self.state, self.info = State.failed, (None,)

    def closed_list(self):
        return self.closed_hash_table.itervalues()

    def is_complete(self):
        return self.state == State.failed or self.state == State.success

    def open_list(self):
        return self.open_heap_queue

    def step(self):
        if self.state == State.start or \
           self.state == State.expand_node_complete:

            if self.open_heap_queue:
                # Retrieve current node from 'open list':
                self.node = heapq.heappop(self.open_heap_queue)
                del self.open_hash_table[self.node.state]

                # Add current node to 'closed list':
                self.closed_hash_table[self.node.state] = self.node

                if self.problem.goal_test(self.node.state):
                    solution = Solution(self.node)
                    self.state, self.info = State.success, (self.node, solution)
                else:
                    self.state, self.info = State.expand_node_begin, (self.node,)
            else:
                self.state, self.info = State.failed, (None,)

            return self.state, (self.info,)
        else:
            if self.state == State.expand_node_begin:
                self.successors = self.problem.successors(self.node)

            successor = next(self.successors, None)

            if successor:
                self.__handle_successor(successor)
            else:
                self.state, self.info = State.expand_node_complete, (self.node,)

            return self.state, self.info

    def __handle_successor(self, successor):
        open_entry = self.open_hash_table.get(successor.state)
        closed_entry = None if open_entry else \
            self.closed_hash_table.get(successor.state)

        if not open_entry and not closed_entry:
            is_successor_state_unique = True

            successor_node = successor.build_node()

            # Add successor node to 'open list':
            heapq.heappush(self.open_heap_queue, successor_node)
            self.open_hash_table[successor_node.state] = successor_node
        else:
            is_successor_state_unique = False

            successor_node = open_entry or closed_entry
            new_path_cost  = self.node.path_cost + successor.step_cost

            if new_path_cost < successor_node.path_cost:
                successor_node.attach(self.node, new_path_cost)

                if closed_entry:
                    successor_node.propagate(self.problem)

                # Values for nodes in 'open list' may have changed:
                heapq.heapify(self.open_heap_queue)

        self.node.add_child(successor_node,
                            successor.action,
                            successor.step_cost)

        self.state, self.info = State.generate_nodes, \
            (self.node, successor_node, is_successor_state_unique)
