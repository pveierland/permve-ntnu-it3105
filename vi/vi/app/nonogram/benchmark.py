import sys

import vi.app.nonogram

def main():
    with open(sys.argv[1], 'r') as f:
        vi.app.nonogram.build_problem(f.read())
