#!/usr/bin/python3

import argparse
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../vi'))

import vi.app.sudoku
import vi.csp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('puzzle_input_filename')
    parser.add_argument('--general', action='store_true')
    parser.add_argument('--pdf', metavar='output_filename')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    input_network = vi.app.sudoku.load_network(
        args.puzzle_input_filename, args.general)

    result_network, statistics = vi.csp.backtrack_search(input_network)

    if result_network:
        puzzle = vi.app.sudoku.convert_network_to_puzzle(result_network)

        if args.pdf:
            vi.app.sudoku.render_output(args.pdf, puzzle)

        if args.verbose:
            print(puzzle)

        format_string = 'Variables: {1} Constraints: {2} ' + \
                        'Backtrack calls: {3} Backtrack failures: {4}' \
                        if args.verbose else \
                        '\\texttt{{{0}}} & {1} & {2} & {3} & {4}'

        print(format_string.format(
                  os.path.split(args.puzzle_input_filename)[-1],
                  len(result_network.variables),
                  len(result_network.constraints),
                  statistics.calls,
                  statistics.failures))

        return 0
    else:
        if args.verbose:
            print("Failed to solve Sudoku.", file=sys.stderr)

        return -1

    print(statistics)

if __name__ == '__main__':
    sys.exit(main())
