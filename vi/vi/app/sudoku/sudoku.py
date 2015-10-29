#!/usr/bin/python3

import argparse
import sys

import vi.app.sudoku
import vi.csp
import vi.search.graph

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('puzzle_input_filename')
    parser.add_argument('--pdf', metavar='output_filename')
    args = parser.parse_args()

    problem = vi.app.sudoku.load_problem(args.puzzle_input_filename)
    #search  = vi.search.graph.BestFirst(problem)
    
    print(vi.app.sudoku.convert_network_to_puzzle(problem))

    network, statistics = vi.csp.backtrack_search(problem)
    print(vi.app.sudoku.convert_network_to_puzzle(network))
    print(statistics)

#    if search.search():
#        puzzle = vi.app.sudoku.convert_network_to_puzzle(search.node.state)
#
#        print('num_open={0} num_closed={1} cost={2}'.format(
#            len(search.open_list()),
#            len(search.closed_list()),
#            search.info[1].cost))
#
#        if args.pdf:
#            vi.app.sudoku.render_output(args.pdf, puzzle)
#        else:
#            print(puzzle)
#        return 0
#    else:
#        print("Failed to solve Sudoku.", file=sys.stderr)
#        return -1

if __name__ == '__main__':
    sys.exit(main())
