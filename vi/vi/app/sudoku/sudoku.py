#!/usr/bin/python3

import sys

import vi.app.sudoku
import vi.search.graph

def main():
    problem = vi.app.sudoku.load_problem(sys.argv[1])
    search  = vi.search.graph.BestFirst(problem)

    if search.search():
        print(vi.app.sudoku.convert_network_to_puzzle(search.node.state))

    #while True:
    #    if search.state is vi.search.graph.State.start or \
    #       search.state is vi.search.graph.State.expand_node_begin:
    #        print(vi.app.sudoku.convert_network_to_puzzle(search.node.state))

    #    search.step()

    #    if search.is_complete():
    #        break

    #    #vi.app.sudoku.render_output('wat.pdf', None)

if __name__ == '__main__':
    main()
