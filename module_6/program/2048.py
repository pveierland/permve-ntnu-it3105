#!/usr/bin/python

from visuals import GameWindow

import argparse
import ai2048demo
import copy
import numpy
import math
import struct
import random
import sys
import pickle
import theano
import theano.tensor as T

from sklearn.utils import shuffle

sys.path.append('../../vi')
import vi.theano

# Directions, DO NOT MODIFY
UP    = 0
DOWN  = 1
LEFT  = 2
RIGHT = 3

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = { UP:    ( 1,  0),
            DOWN:  (-1,  0),
            LEFT:  ( 0,  1),
            RIGHT: ( 0, -1) }

def merge(line):
    # Helper function that merges a single row or column in 2048
    # Move all non-zero values of list to the left
    nonzeros_removed = []
    result = []
    merged = False
    for number in line:
        if number != 0:
            nonzeros_removed.append(number)

    while len(nonzeros_removed) != len(line):
        nonzeros_removed.append(0)

    # Double sequental tiles if same value
    for number in range(0, len(nonzeros_removed) - 1):
        if nonzeros_removed[number] == nonzeros_removed[number + 1] and merged == False:
            result.append(nonzeros_removed[number] * 2)
            merged = True
        elif nonzeros_removed[number] != nonzeros_removed[number + 1] and merged == False:
            result.append(nonzeros_removed[number])
        elif merged == True:
            merged = False

    if nonzeros_removed[-1] != 0 and merged == False:
        result.append(nonzeros_removed[-1])

    while len(result) != len(nonzeros_removed):
        result.append(0)

    return result

# https://github.com/jbutewicz/An-Introduction-to-Interactive-Programming-in-Python/blob/master/Principles%20of%20Computing%20Week%201/2048.py
# Modified for convenience.
class TwentyFortyEight:
    # Class to run the game logic.
    # Compute inital row dictionary to make move code cleaner
    initial = {
        UP : [[0,element] for element in range(4)],
        DOWN : [[4 - 1, element] for element in range(4)],
        LEFT : [[element, 0] for element in range(4)],
        RIGHT : [[element, 4 - 1] for element in range (4)]
    }

    def __init__(self):
        self.reset()

    def __str__(self):
        # Print a string representation of the grid for debugging.
        for number in range(0, 4):
            print(self.cells[number])

    def can_move(self, direction):
        temp = copy.deepcopy(self.cells)
        result = self.move(direction, with_spawn=False)
        self.cells = temp
        return result

    def count_free(self):
        return sum(cell == 0 for row in self.cells for cell in row)

    def count_merges(self):
        def count_line_merges(line):
            merges  = 0
            prev    = 0
            counter = 0

            for i in range(4):
                rank = line[i]
                if rank:
                    if prev == rank:
                        counter += 1
                    elif counter > 0:
                        merges += 1 + counter
                        counter = 0
                    prev = rank

            if counter > 0:
                merges += 1 + counter

            return merges

        return (count_line_merges(self.cells[0]) +
                count_line_merges(self.cells[1]) +
                count_line_merges(self.cells[2]) +
                count_line_merges(self.cells[3]) +
                count_line_merges([self.cells[0][0], self.cells[1][0], self.cells[2][0], self.cells[3][0]]) +
                count_line_merges([self.cells[0][1], self.cells[1][1], self.cells[2][1], self.cells[3][1]]) +
                count_line_merges([self.cells[0][2], self.cells[1][2], self.cells[2][2], self.cells[3][2]]) +
                count_line_merges([self.cells[0][3], self.cells[1][3], self.cells[2][3], self.cells[3][3]]))

    def get_highest_tile(self):
        return max(cell for row in self.cells for cell in row)

    def get_tile(self, row, col):
        # Return the value of the tile at position row, col.
        return self.cells[row][col]

    def is_game_over(self):
        return not any(self.can_move(direction) for direction in [UP, DOWN, LEFT, RIGHT])

    def move(self, direction, with_spawn=True):
        # Move all tiles in the given direction and add
        # a new tile if any tiles moved.
        initial_list = self.initial[direction]
        temporary_list = []

        if(direction == UP):
            return self.move_helper(initial_list, direction, temporary_list, with_spawn)
        elif(direction == DOWN):
            return self.move_helper(initial_list, direction, temporary_list, with_spawn)
        elif(direction == LEFT):
            return self.move_helper(initial_list, direction, temporary_list, with_spawn)
        elif(direction == RIGHT):
            return self.move_helper(initial_list, direction, temporary_list, with_spawn)

    def move_helper(self, initial_list, direction, temporary_list, with_spawn):
        # Move all columns and merge
        self.cells_before = copy.deepcopy(self.cells)

        for element in initial_list:
            temporary_list.append(element)

            for index in range(1, 4):
                temporary_list.append([x + y for x, y in zip(temporary_list[-1], OFFSETS[direction])])

            indices = []

            for index in temporary_list:
                indices.append(self.get_tile(index[0], index[1]))

            merged_list = merge(indices)

            for index_x, index_y in zip(merged_list, temporary_list):
                self.set_tile(index_y[0], index_y[1], index_x)

            temporary_list = []

        if self.cells_before != self.cells:
            if with_spawn:
                self.new_tile()
            return True
        else:
            return False

    def new_tile(self):
        # Create a new tile in a randomly selected empty
        # square.  The tile should be 2 90% of the time and
        # 4 10% of the time.
        available_positions = []
        for row in range(4):
            for col in range(4):
                if self.cells[row][col] == 0:
                    available_positions.append([row, col])

        if not available_positions:
            return False
        else:
            random_tile = random.choice(available_positions)

            weighted_choices = [(2, 9), (4, 1)]
            population = [val for val, cnt in weighted_choices for i in range(cnt)]
            tile = random.choice(population)

            self.set_tile(random_tile[0],random_tile[1], tile)

            return True

    def reset(self):
        # Reset the game so the grid is empty.
        self.cells = [[0 for col in range(4)] for row in range(4)]
        self.cells_before = copy.deepcopy(self.cells)

    def set_tile(self, row, col, value):
        # Set the tile at position row, col to have the given value.
        self.cells[row][col] = value

    def undo_move(self):
        self.cells = self.cells_before

def generate_training_data():
    game = TwentyFortyEight()
    game.new_tile()

    xdata = []
    ydata = []

    while not game.is_game_over():
        x = transform_state(game)
        y = greedy_move_selector(game)

        xdata.append(x)
        ydata.append(y)

        game.move(y)

    return game.get_highest_tile(), xdata, ydata

def greedy_move_selector(game):
    def score_move(move):
        free_before    = game.count_free()
        merges_before  = game.count_merges()
        actual_move    = game.move(move, with_spawn=False)
        free_after     = game.count_free()
        merges_after   = game.count_merges()
        game.undo_move()

        return (10 * (free_after - free_before) + (merges_after - merges_before)) if actual_move else -1000

    best_move_score, best_move = max((score_move(move), move) for move in [UP, DOWN, LEFT, RIGHT])

    return best_move

def play_ai_game():
    game = TwentyFortyEight()
    game.new_tile()

    while not game.is_game_over():
        game.move(greedy_move_selector(game))

    return game.get_highest_tile()

def play_random_game():
    game = TwentyFortyEight()
    game.new_tile()

    while not game.is_game_over():
        game.move(random.choice([UP, DOWN, LEFT, RIGHT]))

    return game.get_highest_tile()

def transform_state(game, delta=False):
    def get_successor_values(move):
        game.move(move, with_spawn=False)
        free   = game.count_free()
        merges = game.count_merges()
        game.undo_move()
        return free, merges

    current_free   = game.count_free()
    current_merges = game.count_merges()

    free_up, merges_up       = get_successor_values(UP)
    free_down, merges_down   = get_successor_values(DOWN)
    free_left, merges_left   = get_successor_values(LEFT)
    free_right, merges_right = get_successor_values(RIGHT)

    if delta:
        return [ free_up - current_free, free_down - current_free, free_left - current_free, free_right - current_free,
                 merges_up - current_merges, merges_down - current_merges, merges_left - current_merges, merges_right - current_merges ]
    else:
        return [ current_free, current_merges, free_up, merges_up, free_down, merges_down, free_left, merges_left, free_right, merges_right ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--L1', type=float)
    parser.add_argument('--L2', type=float)
    parser.add_argument('--data', default='training_data.pkl')
    parser.add_argument('--dropout', type=float)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--hidden_function', default='relu')
    parser.add_argument('--hidden_layers', nargs='*')
    parser.add_argument('--learning_rate', type=float, default=0.005)
    parser.add_argument('--generate', type=int)
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--max_time', type=int)
    parser.add_argument('--minibatch_size', type=int, default=40)
    parser.add_argument('--model', default='model.pkl')
    parser.add_argument('--output_directory', default='../data')
    parser.add_argument('--runs', action='store_true')
    parser.add_argument('--seed', type=int)
    parser.add_argument('--training_ratio', type=float)
    args = parser.parse_args()

    print(args)

    if args.generate:
        training_data   = []
        training_labels = []

        for i in range(args.generate):
            top_tile, x, y = generate_training_data()
            training_data.extend(x)
            training_labels.extend(y)

            print('{}/{} ({:.2f}%)'.format(i + 1, args.generate, 100.0 * (i + 1) / args.generate))

        print('{} examples generated from {} games'.format(len(training_data), args.generate))

        training_data, training_labels = shuffle(training_data, training_labels, random_state=0)

        with open(args.data, 'wb') as training_data_file:
            pickle.dump((training_data, training_labels), training_data_file)
    elif args.demo:
        network = pickle.load(open(args.model, 'rb'))

        predict_function = theano.function(
            inputs=[network.inputs],
            outputs=network.layers[-1].testing_outputs)

        La = []

        for _ in range(50):
            game = TwentyFortyEight()
            game.new_tile()

            while not game.is_game_over():
                input = numpy.asarray(transform_input(game.cells))
                move_probabilities = predict_function(input.reshape(1, input.shape[0]))[0]
                move_probabilities_sorted = sorted(((probability, move) for (move, probability) in enumerate(move_probabilities)), reverse=True)

                # Select the first valid move ranked by probability:
                for probability, move in move_probabilities_sorted:
                    if game.move(move + 1):
                        break

            t = game.get_highest_tile()
            print(t)
            La.append(t)

        Lr = list(play_random_game() for _ in range(50))

        print('random play: {}'.format(Lr))
        print('ann play: {}'.format(La))
        print(ai2048demo.welch(Lr, La))

#
# def do_training():
#     def epoch_status_function(time, epoch, average_loss, testing_error, is_best):
#         if is_best:
#             with open('model.pkl', 'wb') as model_file:
#                 pickle.dump(network, model_file)
#
#         print("Time: {:7.2f} sec, Epoch: {:4d}, Testing error: {:.5f}%".format(
#             time, epoch, testing_error * 100.0))
#
#
#     x_data, y_data = pickle.load(open('training_data.pkl', 'rb'))
#     #x_data, y_data = shuffle(x_data, y_data, random_state=0)
#
#     y_data = [ y - 1 for y in y_data ]
#
#     training_ratio = 0.1
#
#     num_training_examples = int(math.ceil(training_ratio * len(x_data)))
#
#     minibatch_size = 20
#     learning_rate = 0.08
#     epochs = 100
#
#     layer_sizes = [len(x_data[0])] + [512] + [4]
#
#     print("Creating shared Theano dataset variables...")
#
#     training_dataset = vi.theano.TheanoDataSet(
#         theano.shared(numpy.asarray(x_data[:num_training_examples], dtype=theano.config.floatX), borrow=True),
#         T.cast(theano.shared(numpy.asarray(y_data[:num_training_examples], dtype=theano.config.floatX), borrow=True), 'int32'),
#         num_training_examples)
#
#     minibatch_index = T.lscalar()
#     x               = T.matrix('x')
#     y               = T.ivector('y')
#
#     network = vi.theano.Network(
#         x, layer_sizes, theano.tensor.nnet.relu, None, None, None)
#         #x, layer_sizes, theano.tensor.nnet.relu, 0.8, None, 0.0001)
#
#     training_minibatch_count = math.ceil(training_dataset.size / minibatch_size)
#
#     loss_function = network.loss_function(y)
#     parameters    = network.parameters()
#
#     gradients = [
#         T.grad(loss_function, parameter)
#         for parameter in parameters
#     ]
#
#     updates = [
#         (parameter, parameter - learning_rate * gradient)
#         for parameter, gradient in zip(parameters, gradients)
#     ]
#
#     training_function = theano.function(
#         inputs  = [minibatch_index],
#         outputs = network.errors(y),
#         updates = updates,
#         givens  = {
#             x: training_dataset.data  [minibatch_index * minibatch_size : (minibatch_index + 1) * minibatch_size],
#             y: training_dataset.labels[minibatch_index * minibatch_size : (minibatch_index + 1) * minibatch_size]
#         }
#     )
#
#     testing_function = theano.function(
#         inputs  = [minibatch_index],
#         outputs = network.errors(y),
#         givens  = {
#             x: training_dataset.data  [minibatch_index * minibatch_size:(minibatch_index + 1) * minibatch_size],
#             y: training_dataset.labels[minibatch_index * minibatch_size:(minibatch_index + 1) * minibatch_size]
#         }
#     )
#
#     print("Starting stochastic gradient descent. learning_rate={} epochs={}".format(
#         learning_rate, epochs))
#
#     training_time, training_epochs, testing_error = \
#         vi.theano.stochastic_gradient_descent(
#             training_function,
#             training_minibatch_count,
#             testing_function,
#             training_minibatch_count,
#             learning_rate=learning_rate,
#             epochs=epochs,
#             epoch_status_function=epoch_status_function)
#
#     print(("Training completed after {:.2f} seconds. {} epochs at {:.2f} epochs / second. " +
#            "Testing error: {:.5f}%").format(
#         training_time,
#         training_epochs,
#         training_epochs / training_time,
#         testing_error * 100.0))






#32	8
#64	16
#128	21
#256	5


#window = GameWindow( )
#window.update_view(flatstuff(g.cells))
#window.mainloop()


if __name__ == "__main__":
    main()