import enum
import collections
import heapq

from vi.search.graph import Solution, State

class BestFirst(object):
    class Strategy(enum.Enum):
        breadth_first = 1
        depth_first   = 2
        dijkstra      = 3
        astar         = 4

    def __init__(self, problem, strategy=None):
        self.problem  = problem
        self.strategy = strategy or BestFirst.Strategy.astar

        self.open_deque        = collections.deque()
        self.open_heap_queue   = []
        self.open_hash_table   = {}
        self.closed_hash_table = {}

        self.node = self.problem.initial_node()

        if self.node:
            if self.strategy is BestFirst.Strategy.astar:
                self.node.apply_heuristic(self.problem)

            self.__push_open(self.node)
            self.__set_state(State.start, self.node)
        else:
            self.__set_state(State.failed)

    def closed_list(self):
        return self.closed_hash_table.values()

    def is_complete(self):
        return self.state is State.failed or self.state is State.success

    def open_list(self):
        return self.open_hash_table.values()

    def set_strategy(self, strategy):
        if (self.strategy is BestFirst.Strategy.dijkstra or \
            self.strategy is BestFirst.Strategy.astar) and \
           (strategy is BestFirst.Strategy.breadth_first or \
            strategy is BestFirst.Strategy.depth_first):

            while self.open_heap_queue:
                node = heapq.heappop(self.open_heap_queue)
                node.clear_heuristic()
                self.open_deque.append(node)

            for node in self.closed_hash_table.values():
                node.clear_heuristic()

        elif (self.strategy is BestFirst.Strategy.breadth_first or \
              self.strategy is BestFirst.Strategy.depth_first) and \
             (strategy is BestFirst.Strategy.dijkstra or \
              strategy is BestFirst.Strategy.astar):

            while self.open_deque:
                node = self.open_deque.popleft()

                if strategy is BestFirst.Strategy.astar:
                    node.apply_heuristic(self.problem)

                heapq.heappush(self.open_heap_queue, node)

            if strategy is BestFirst.Strategy.astar:
                for node in self.closed_hash_table.values():
                    node.apply_heuristic(self.problem)

        elif self.strategy is BestFirst.Strategy.dijkstra and \
             strategy is BestFirst.Strategy.astar:

            for node in self.open_heap_queue:
                node.apply_heuristic(self.problem)

            for node in self.closed_hash_table.values():
                node.apply_heuristic(self.problem)

            self.__open_list_costs_changed()
        elif self.strategy is BestFirst.Strategy.astar and \
             strategy is BestFirst.Strategy.dijkstra:

            for node in self.open_heap_queue:
                node.clear_heuristic()

            for node in self.closed_hash_table.values():
                node.clear_heuristic()

            self.__open_list_costs_changed()

        self.strategy = strategy

    def search(self):
        while not self.is_complete():
            self.step()
        if self.state == State.success:
            return self.info[1]

    def step(self):
        if self.state is State.start or \
           self.state is State.expand_node_complete:

            if not self.__is_open_queue_empty():
                self.node = self.__pop_open()
                self.__push_closed(self.node)

                if self.problem.goal_test(self.node.state):
                    solution = self.__create_solution(self.node)
                    self.__set_state(State.success, self.node, solution)
                else:
                    self.__set_state(State.expand_node_begin, self.node)
            else:
                self.__set_state(State.failed, self.node)
        else:
            if self.state is State.expand_node_begin:
                self.successors = self.problem.successors(self.node)

            successor = next(self.successors, None)

            if successor:
                self.__handle_successor(successor)
            else:
                self.__set_state(State.expand_node_complete, self.node)

    def __create_solution(self, node):
        return self.problem.solution(node) \
               if hasattr(self.problem, 'solution') \
               else Solution(node)

    def __handle_successor(self, successor):
        open_entry = self.open_hash_table.get(successor.state)
        closed_entry = None if open_entry else \
            self.closed_hash_table.get(successor.state)

        if not open_entry and not closed_entry:
            is_successor_state_unique = True

            successor_node = successor.build_node()

            if self.strategy is BestFirst.Strategy.astar:
                successor_node.apply_heuristic(self.problem)

            self.__push_open(successor_node)
        else:
            is_successor_state_unique = False

            successor_node = open_entry or closed_entry

            if self.strategy is BestFirst.Strategy.astar:
                new_path_cost = self.node.path_cost + successor.step_cost

                if new_path_cost < successor_node.path_cost:
                    successor_node.attach(self.node, new_path_cost)

                    if closed_entry:
                        successor_node.propagate()

                    self.__open_list_costs_changed()

        if self.strategy is BestFirst.Strategy.astar:
            self.node.add_child(successor_node,
                                successor.action,
                                successor.step_cost)

        self.__set_state(State.generate_nodes,
                         self.node,
                         successor_node,
                         is_successor_state_unique)

    def __is_open_queue_empty(self):
        if self.strategy is BestFirst.Strategy.dijkstra or \
           self.strategy is BestFirst.Strategy.astar:
            return len(self.open_heap_queue) == 0
        elif self.strategy is BestFirst.Strategy.breadth_first or \
             self.strategy is BestFirst.Strategy.depth_first:
            return len(self.open_deque) == 0

    def __open_list_costs_changed(self):
        if self.strategy is BestFirst.Strategy.dijkstra or \
           self.strategy is BestFirst.Strategy.astar:
            heapq.heapify(self.open_heap_queue)

    def __pop_open(self):
        if self.strategy is BestFirst.Strategy.dijkstra or \
           self.strategy is BestFirst.Strategy.astar:
            node = heapq.heappop(self.open_heap_queue)
        elif self.strategy is BestFirst.Strategy.breadth_first or \
             self.strategy is BestFirst.Strategy.depth_first:
            node = self.open_deque.popleft()

        del self.open_hash_table[node.state]

        return node

    def __push_closed(self, node):
        self.closed_hash_table[node.state] = node

    def __push_open(self, node):
        if self.strategy is BestFirst.Strategy.dijkstra or \
           self.strategy is BestFirst.Strategy.astar:
            heapq.heappush(self.open_heap_queue, node)
        elif self.strategy is BestFirst.Strategy.depth_first:
            self.open_deque.appendleft(node)
        elif self.strategy is BestFirst.Strategy.breadth_first:
            self.open_deque.append(node)

        self.open_hash_table[node.state] = node

    def __set_state(self, state, *info):
        self.state = state
        self.info  = info
