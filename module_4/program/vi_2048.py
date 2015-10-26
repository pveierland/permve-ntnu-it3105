#!/usr/bin/python

import vi_2048
import visuals

gameWindow = visuals.GameWindow()
vi_2048.reset_game()

while True:
    state = vi_2048.step_game()

    if not state:
        break

    gameWindow.update_view(
        [ (state >> (4 * column + 16 * row)) & 0xF
          for row in range(4) for column in range(4) ] )

# Don't close window
raw_input()

