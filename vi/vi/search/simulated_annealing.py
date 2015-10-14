import math
import random

def simulated_annealing(problem, goal=None, max_epochs=None):
    current        = problem.initial()
    current_energy = problem.evaluate(current)

    epoch = 0

    while not max_epochs or epoch != max_epochs:
        temperature = problem.temperature(epoch)

        if not temperature:
            break

        successor        = problem.random_successor(current)
        successor_energy = problem.evaluate(successor)

        # Successor state energy must be non-negative for the state to be valid:
        if successor_energy >= 0:
            if goal and successor_energy >= goal:
                return (successor, epoch)

            delta_energy = successor_energy - current_energy

            if delta_energy > 0:
                current        = successor
                current_energy = problem.evaluate(successor)
            else:
                probability = math.exp(float(delta_energy) / temperature)

                if random.random() < probability:
                    current        = successor
                    current_energy = problem.evaluate(successor)

        epoch = epoch + 1

    return (current, epoch)
