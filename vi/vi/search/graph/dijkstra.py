import heapq

from vi.search.graph import Solution, State

class Dijkstra(object):
    def __push_open(node):
        self.open_heap_queue.append(self.node)
        self.open_hash_table[self.node.state] = self.node

    def pop_open():


    def __push_closed(node):
        self.closed_hash_table[self.node.state] = self.node


    def __init__(self, problem):
        self.problem = problem
        self.node    = self.problem.initial_node()

        if self.node:
            self.open_heap_queue   = []
            self.open_hash_table   = {}
            self.closed_hash_table = {}
            
            if self.problem.goal_test(self.node.state):
                self.__push_closed(self.node)
                self.__set_state(State.success, self.node, Solution(self.node))
            else:
                self.__push_open(self.node)
                self.__set_state(State.start, self.node)
        else:
            self.__set_state(State.failed)

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
                self.node = self.pop_open()
                self.__push_closed(self.node)

                if self.problem.goal_test(self.node.state):
                    self.__set_state(State.success,
                                     self.node,
                                     Solution(self.node))
                else:
                    self.__set_state(State.expand_node_begin, self.node)
            else:
                self.__set_state(State.failed)
        else:
            if self.state == State.expand_node_begin:
                self.successors = self.problem.successors(self.node)

            successor = next(self.successors, None)

            if successor:




                self.__handle_successor(successor)
            else:
                self.__set_state(State.expand_node_complete, self.node)
        
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
