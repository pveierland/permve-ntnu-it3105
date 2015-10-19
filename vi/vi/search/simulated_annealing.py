import math
import random

def simulated_annealing(
    problem, start_temperature, delta_temperature, max_epochs=None):

    current        = problem.initial()
    current_energy = problem.evaluate(current)

    temperature = start_temperature
    epoch       = 0

    while not max_epochs or epoch != max_epochs:
        if temperature <= 0 or \
           hasattr(problem, 'is_terminal') and \
           problem.is_terminal(current):
            break

        successor        = problem.random_successor(current)
        successor_energy = problem.evaluate(successor)

        # Successor state energy must be non-negative for the state to be valid:
        if successor_energy >= 0:
            delta_energy = successor_energy - current_energy

            if delta_energy > 0:
                current        = successor
                current_energy = problem.evaluate(successor)
            else:
                probability = math.exp(float(delta_energy) / temperature)

                if random.random() < probability:
                    current        = successor
                    current_energy = problem.evaluate(successor)

            temperature = temperature - delta_temperature
            epoch       = epoch + 1

    return (current, epoch)
