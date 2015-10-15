import random
import sys

from vi.games.twentyfortyeight import expectiminimax, heuristic, NodeType, State
from vi.search.grid import Action

def game():
    def populate(state):
        available = state.available()
        if available:
            state.set_value(*random.choice(state.available()),
                            value=2 if random.random() < 0.9 else 4)
            return True
        else:
            return False

    state = State()

    #populate(state)
    #populate(state)
    #populate(state)
    #populate(state)
    #populate(state)
    #populate(state)
    #populate(state)
    #populate(state)

    while True:
        if not populate(state):
            print("GAME OVER! HIGHEST TILE = {0}".format(
                  state.get_highest_value()))
            sys.exit(-1)

        score, move = expectiminimax(NodeType.player, state, 4)
        state = state.move(move)

        print('{0} {1}\n{2}\n'.format(score, heuristic(state), state))

if __name__ == '__main__':
    game()
