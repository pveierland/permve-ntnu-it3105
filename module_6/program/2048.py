#!/usr/bin/python

#from visuals import GameWindow

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
    @staticmethod
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

    # Class to run the game logic.
    # Compute inital row dictionary to make move code cleaner
    initial = {
        UP : [[0,element] for element in range(4)],
        DOWN : [[4 - 1, element] for element in range(4)],
        LEFT : [[element, 0] for element in range(4)],
        RIGHT : [[element, 4 - 1] for element in range (4)]
    }

    def __init__(self, state=None):
        if state:
            self.cells = state
        else:
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

    def copy_and_set_tile(self, row, col, value):
        new = TwentyFortyEight(self.cells)
        new.set_tile(row, col, value)
        return new

    def count_free(self):
        return sum(cell == 0 for row in self.cells for cell in row)

    def count_merges(self):
        return self.count_horizontal_merges() + \
               self.count_vertical_merges()

    def count_horizontal_merges(self):
        return (self.count_line_merges(self.cells[0]) +
                self.count_line_merges(self.cells[1]) +
                self.count_line_merges(self.cells[2]) +
                self.count_line_merges(self.cells[3]))

    def count_vertical_merges(self):
        return (self.count_line_merges([self.cells[0][0], self.cells[1][0], self.cells[2][0], self.cells[3][0]]) +
               self.count_line_merges([self.cells[0][1], self.cells[1][1], self.cells[2][1], self.cells[3][1]]) +
               self.count_line_merges([self.cells[0][2], self.cells[1][2], self.cells[2][2], self.cells[3][2]]) +
               self.count_line_merges([self.cells[0][3], self.cells[1][3], self.cells[2][3], self.cells[3][3]]))

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

def generate_training_data(representation):
    game = TwentyFortyEight()
    game.new_tile()

    xdata = []
    ydata = []

    while not game.is_game_over():
        num_free     = game.count_free()
        moves_scored = sorted(((score_move(game, representation, move) - num_free, move) for move in range(4)), reverse=True)
        best_move    = moves_scored[0][1]

        # Only use as training example if delta is positive and move is scored better than any other move:
        if moves_scored[0][0] > 0 and any(moves_scored[i][0] != moves_scored[0][0] for i in range(1, 4)):
            x = transform_state(game, representation)
            y = best_move

            xdata.append(x)
            ydata.append(y)

        game.move(best_move)

    return game.get_highest_tile(), xdata, ydata

def score_move(game, representation, move):
    if game.move(move, with_spawn=False):
        score = game.count_free()
        game.undo_move()
        return score
    else:
        return -1

def play_ann_game(representation, predict_function):
    game = TwentyFortyEight()
    game.new_tile()

    while not game.is_game_over():
        x = numpy.asarray(transform_state(game, representation))
        move_probabilities = predict_function(x.reshape(1, x.shape[0]))[0]
        move_probabilities_sorted = sorted(((probability, move) for (move, probability) in enumerate(move_probabilities)), reverse=True)

        # Select the first valid move ranked by probability:
        for probability, move in move_probabilities_sorted:
            if game.move(move):
                break

    t = game.get_highest_tile()
    print(t)
    return t

def play_ai_game(representation):
    game = TwentyFortyEight()
    game.new_tile()

    while not game.is_game_over():
        game.move(max((score_move(game, representation, move), move) for move in range(4))[1])

    return game.get_highest_tile()

def play_random_game():
    game = TwentyFortyEight()
    game.new_tile()

    while not game.is_game_over():
        game.move(random.choice([UP, DOWN, LEFT, RIGHT]))

    return game.get_highest_tile()

def transform_state(game, representation):
    if not representation:
        # Representation A:
        return [ TwentyFortyEight.count_line_merges(game.cells[0]),
                 TwentyFortyEight.count_line_merges(game.cells[1]),
                 TwentyFortyEight.count_line_merges(game.cells[2]),
                 TwentyFortyEight.count_line_merges(game.cells[3]),
                 TwentyFortyEight.count_line_merges([game.cells[0][0], game.cells[1][0], game.cells[2][0], game.cells[3][0]]),
                 TwentyFortyEight.count_line_merges([game.cells[0][1], game.cells[1][1], game.cells[2][1], game.cells[3][1]]),
                 TwentyFortyEight.count_line_merges([game.cells[0][2], game.cells[1][2], game.cells[2][2], game.cells[3][2]]),
                 TwentyFortyEight.count_line_merges([game.cells[0][3], game.cells[1][3], game.cells[2][3], game.cells[3][3]]) ]
    else:
        # Representation B:
        values         = [ game.cells[row][column] for row in range(4) for column in range(4) ]
        unique_nonzero = sorted(list(set(values) - set([0])))
        return [ (unique_nonzero.index(value) + 1 if value in unique_nonzero else 0) for value in values ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--A', action='store_true')
    parser.add_argument('--B', action='store_true')
    parser.add_argument('--L1', type=float)
    parser.add_argument('--L2', type=float)
    parser.add_argument('--ai', action='store_true')
    parser.add_argument('--benchmark', type=int)
    parser.add_argument('--compare', type=int)
    parser.add_argument('--data_a', default='training_data_a.pkl')
    parser.add_argument('--data_b', default='training_data_b.pkl')
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--dropout', type=float)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--generate', type=int)
    parser.add_argument('--hidden_function', default='relu')
    parser.add_argument('--hidden_layers', nargs='*')
    parser.add_argument('--learning_rate', type=float, default=0.08)
    parser.add_argument('--max_time', type=int)
    parser.add_argument('--minibatch_size', type=int, default=40)
    parser.add_argument('--model_a', default='model_a.pkl')
    parser.add_argument('--model_b', default='model_b.pkl')
    parser.add_argument('--output_directory', default='../data')
    parser.add_argument('--runs', action='store_true')
    parser.add_argument('--seed', type=int)
    parser.add_argument('--training_ratio', type=float)
    args = parser.parse_args()

    if not args.A and not args.B and not args.compare:
        print('A or B representation must be chosen!')
        sys.exit(-1)

    print(args)

    if args.ai:
        if args.benchmark:
            La = list(play_ai_game(args.B) for _ in range(args.benchmark))
            print('mean: {} std: {}'.format(numpy.mean(La), numpy.std(La)))
        else:
            Lr = list(play_random_game() for _ in range(50))
            La = list(play_ai_game(args.B) for _ in range(50))

            print('random play: {}'.format(Lr))
            print('ann play: {}'.format(La))
            print(ai2048demo.welch(Lr, La))
    elif args.benchmark:
        network = pickle.load(open(args.model_a if args.A else args.model_b, 'rb'))

        predict_function = theano.function(
            inputs=[network.inputs],
            outputs=network.layers[-1].testing_outputs,
            allow_input_downcast=True)

        La = [ play_ann_game(args.B, predict_function) for _ in range(args.benchmark) ]
        print('mean: {} std: {}'.format(numpy.mean(La), numpy.std(La)))

    elif args.generate:
        training_data   = []
        training_labels = []

        for i in range(args.generate):
            top_tile, x, y = generate_training_data(args.B)
            training_data.extend(x)
            training_labels.extend(y)

            print('{}/{} ({:.2f}%)'.format(i + 1, args.generate, 100.0 * (i + 1) / args.generate))

        print('{} examples generated from {} games'.format(len(training_data), args.generate))

        training_examples = list(zip(training_data, training_labels))
        random.shuffle(training_examples)
        training_data[:], training_labels[:] = zip(*training_examples)

        with open(args.data_a if args.A else args.data_b, 'wb') as training_data_file:
            pickle.dump((training_data, training_labels), training_data_file)
    elif args.compare:
        import scipy.stats

        network_a = pickle.load(open(args.model_a, 'rb'))
        network_b = pickle.load(open(args.model_b, 'rb'))

        predict_function_a = theano.function(
            inputs=[network_a.inputs],
            outputs=network_a.layers[-1].testing_outputs,
            allow_input_downcast=True)

        predict_function_b = theano.function(
            inputs=[network_b.inputs],
            outputs=network_b.layers[-1].testing_outputs,
            allow_input_downcast=True)

        La_a = [ play_ann_game(False, predict_function_a) for _ in range(args.compare) ]
        La_b = [ play_ann_game(True,  predict_function_b) for _ in range(args.compare) ]

        statistic, pvalue = scipy.stats.ttest_ind(La_a, La_b, equal_var=False)

        print('statistic = {:f} pvalue = {:f}'.format(statistic, pvalue))

    elif args.demo:
        network = pickle.load(open(args.model_a if args.A else args.model_b, 'rb'))

        predict_function = theano.function(
            inputs=[network.inputs],
            outputs=network.layers[-1].testing_outputs,
            allow_input_downcast=True)

        La = []

        for _ in range(50):
            game = TwentyFortyEight()
            game.new_tile()

            while not game.is_game_over():
                x = numpy.asarray(transform_state(game, args.B))
                move_probabilities = predict_function(x.reshape(1, x.shape[0]))[0]
                move_probabilities_sorted = sorted(((probability, move) for (move, probability) in enumerate(move_probabilities)), reverse=True)

                # Select the first valid move ranked by probability:
                for probability, move in move_probabilities_sorted:
                    if game.move(move):
                        break

            t = game.get_highest_tile()
            print(t)
            La.append(t)

        Lr = list(play_random_game() for _ in range(50))

        print('random play: {}'.format(Lr))
        print('ann play: {}'.format(La))
        print(ai2048demo.welch(Lr, La))
    else:
        def epoch_status_function(time, epoch, average_loss, testing_error, is_best):
            if is_best:
                with open(args.model_a if args.A else args.model_b, 'wb') as model_file:
                    pickle.dump(network, model_file)

            print("Time: {:7.2f} sec, Epoch: {:4d}, Average loss: {:.5f}, Testing error: {:.5f}%".format(
                time, epoch, average_loss, testing_error * 100.0))

        x_data, y_data = pickle.load(open(args.data_a if args.A else args.data_b, 'rb'))
        #x_data, y_data = shuffle(x_data, y_data, random_state=0)

        num_training_examples = int(math.ceil(args.training_ratio * len(x_data))) \
                                if args.training_ratio else len(x_data)

        input_size = len(x_data[0])

        layer_sizes = [input_size] + list(map(int, args.hidden_layers or [])) + [4]

        print("Creating shared Theano dataset variables...")

        training_dataset = vi.theano.TheanoDataSet(
            theano.shared(numpy.asarray(x_data[:num_training_examples], dtype=theano.config.floatX), borrow=True),
            T.cast(theano.shared(numpy.asarray(y_data[:num_training_examples], dtype=theano.config.floatX), borrow=True), 'int32'),
            num_training_examples)

        minibatch_index = T.lscalar()
        x               = T.matrix('x')
        y               = T.ivector('y')

        network = vi.theano.Network(
            x, layer_sizes, theano.tensor.nnet.relu, args.dropout, args.L1, args.L2)

        training_minibatch_count = math.ceil(training_dataset.size / args.minibatch_size)

        loss_function = network.loss_function(y)
        parameters    = network.parameters()

        gradients = [
            T.grad(loss_function, parameter)
            for parameter in parameters
        ]

        updates = [
            (parameter, parameter - args.learning_rate * gradient)
            for parameter, gradient in zip(parameters, gradients)
        ]

        training_function = theano.function(
            inputs  = [minibatch_index],
            outputs = network.errors(y),
            updates = updates,
            givens  = {
                x: training_dataset.data  [minibatch_index * args.minibatch_size : (minibatch_index + 1) * args.minibatch_size],
                y: training_dataset.labels[minibatch_index * args.minibatch_size : (minibatch_index + 1) * args.minibatch_size]
            }
        )

        testing_function = theano.function(
            inputs  = [minibatch_index],
            outputs = network.errors(y),
            givens  = {
                x: training_dataset.data  [minibatch_index * args.minibatch_size:(minibatch_index + 1) * args.minibatch_size],
                y: training_dataset.labels[minibatch_index * args.minibatch_size:(minibatch_index + 1) * args.minibatch_size]
            }
        )

        print("Starting stochastic gradient descent. learning_rate={} epochs={}".format(
            args.learning_rate, args.epochs))

        training_time, training_epochs, testing_error = \
            vi.theano.stochastic_gradient_descent(
                training_function,
                training_minibatch_count,
                testing_function,
                training_minibatch_count,
                learning_rate=args.learning_rate,
                epochs=args.epochs,
                epoch_status_function=epoch_status_function)

        print(("Training completed after {:.2f} seconds. {} epochs at {:.2f} epochs / second. " +
               "Testing error: {:.5f}%").format(
            training_time,
            training_epochs,
            training_epochs / training_time,
            testing_error * 100.0))
            

#window = GameWindow( )
#window.update_view(flatstuff(g.cells))
#window.mainloop()


if __name__ == "__main__":
    main()
