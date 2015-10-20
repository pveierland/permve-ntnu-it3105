#!/usr/bin/python3

import sys

import vi.app.sudoku

def main():
    p = vi.app.sudoku.load_puzzle(sys.argv[1])
    print(p)

if __name__ == '__main__':
    main()
