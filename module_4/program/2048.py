#!/usr/bin/python

import argparse
import sys

import vi_2048_python
#import visuals

parser = argparse.ArgumentParser()
parser.add_argument('depth_limit', type=int)
args = parser.parse_args()

#gameWindow = visuals.GameWindow()
vi_2048_python.reset_game()
vi_2048_python.configure(args.depth_limit)

while True:
    state = vi_2048_python.step_game()

    if not state:
        break

    #gameWindow.update_view(
    #    [ (state >> (4 * column + 16 * row)) & 0xF
    #      for row in range(4) for column in range(4) ] )

# Don't close window
raw_input()

