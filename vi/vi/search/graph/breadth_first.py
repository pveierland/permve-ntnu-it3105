from collections import deque

from vi.search.graph import Solution, State

def breadth_first(problem):
    self.problem = problem

    self.node = self.problem.initial_node()
    
    if self.node:
        if self.problem.goal_test(self.node.state):
            self.state, self.info = State.start, (self.node,)
            return Solution(self.node)

        self.open_deque        = deque([node])
        self.open_hash_table   = {self.node.state: self.node}
        self.closed_hash_table = {}
    else:
        self.state, self.info = State.failed, (None,)

    def closed_list(self):
        return self.closed_hash_table.values()

    def is_complete(self):
        return self.state == State.failed or self.state == State.success

    def open_list(self):
        return self.open_heap_queue

    def step(self):
        if self.state == State.start or \
           self.state == State.expand_node_complete:

            if self.open_heap_queue:
                # Retrieve current node from start of 'open list':
                self.node = open_deque.popleft()
                del self.open_hash_table[self.node.state]

                # Add current node to 'closed list':
                self.closed_hash_table[self.node.state] = self.node
                
                self.state, self.info = State.expand_node_begin, (self.node,)
            else:
                self.state, self.info = State.failed, (None,)
        else:
            if self.state == State.expand_node_begin:
                self.successors = self.problem.successors(self.node)

            successor = next(self.successors, None)

            if successor:
                if self.problem.goal_test(successor.state):
                    # Create solution node + add to 'closed list':
                    self.node = successor.build_node()
                    self.closed_hash_table[self.node.state] = self.node

                    solution = Solution(self.node)
                    self.state, self.info = State.success, (self.node, solution)
                else:
                    existing_entry = self.open_hash_table.get(successor.state) or \
                                     self.closed_hash_table.get(successor.state)

                    if not existing_entry:
                        self.node = successor.build_node()

                        # Add successor node to end of 'open list':
                        heapq.heappush(self.open_heap_queue, successor_node)
                        self.open_hash_table[successor_node.state] = successor_node
            else:
                self.state, self.info = State.expand_node_complete, (self.node,)
            
        return self.state, self.info
