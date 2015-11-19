#!/usr/bin/python3

import argparse
import collections
import math
import numpy
import os
import pickle
import sys
import theano
import theano.tensor as T

sys.path.append('../mnist/basics')
import mnist_basics
import vi.theano

TheanoDataSet = collections.namedtuple('TheanoDataSet', ['data', 'labels', 'size'])

def build_theano_dataset(flat_data, flat_labels):
    data_array   = numpy.asarray(flat_data, dtype=theano.config.floatX)
    data_array  /= 255.0 # Scale to [0-1]
    labels_array = numpy.asarray(flat_labels, dtype=theano.config.floatX)

    shared_data   = theano.shared(data_array, borrow=True)
    shared_labels = T.cast(theano.shared(labels_array, borrow=True), 'int32')

    return TheanoDataSet(shared_data, shared_labels, len(flat_data))

def build_theano_datasets(flat_training_data,
                          flat_training_labels,
                          flat_testing_data,
                          flat_testing_labels,
                          validation_data_ratio):

    validation_example_count = int(validation_data_ratio * len(flat_training_data))

    training_dataset = build_theano_dataset(
        flat_training_data[:-validation_example_count], flat_training_labels[:-validation_example_count])

    validation_dataset = build_theano_dataset(
        flat_training_data[-validation_example_count:], flat_training_labels[-validation_example_count:])

    testing_dataset = build_theano_dataset(flat_testing_data, flat_testing_labels)

    return training_dataset, validation_dataset, testing_dataset

def build_theano_functions(
    network, x, y, minibatch_index, minibatch_size, learning_rate,
    training_dataset, validation_dataset, testing_dataset):

    loss_function = network.loss_function(y)
    parameters    = network.parameters()

    gradients = [
        T.grad(loss_function, parameter)
        for parameter in parameters
    ]

    updates = [
        (parameter, parameter - learning_rate * gradient)
        for parameter, gradient in zip(parameters, gradients)
    ]

    training_function = theano.function(
        inputs  = [minibatch_index],
        outputs = network.errors(y),
        updates = updates,
        givens  = {
            x: training_dataset.data  [minibatch_index * minibatch_size : (minibatch_index + 1) * minibatch_size],
            y: training_dataset.labels[minibatch_index * minibatch_size : (minibatch_index + 1) * minibatch_size]
        }
    )

    testing_function = theano.function(
        inputs  = [minibatch_index],
        outputs = network.errors(y),
        givens  = {
            x: testing_dataset.data  [minibatch_index * minibatch_size:(minibatch_index + 1) * minibatch_size],
            y: testing_dataset.labels[minibatch_index * minibatch_size:(minibatch_index + 1) * minibatch_size]
        }
    )

    validation_function = theano.function(
        inputs  = [minibatch_index],
        outputs = network.errors(y),
        givens  = {
            x: validation_dataset.data  [minibatch_index * minibatch_size:(minibatch_index + 1) * minibatch_size],
            y: validation_dataset.labels[minibatch_index * minibatch_size:(minibatch_index + 1) * minibatch_size]
        }
    )

    return training_function, validation_function, testing_function

def main():
    def epoch_status_function(time, epoch, average_loss, validation_error, testing_error):
        if testing_error:
            with open(os.path.join(base_path, 'model.pkl'), 'wb') as model_file:
                pickle.dump(network, model_file)

        with open(os.path.join(base_path, 'loss.txt'), 'at') as error_file:
            print('{} {:.4f} {:.10f}'.format(epoch, time, average_loss), file=error_file)

        with open(os.path.join(base_path, 'error.txt'), 'at') as error_file:
            print('{} {:.4f} {:.10f}'.format(epoch, time, validation_error * 100.0), file=error_file)

        print("Time: {0:7.2f} sec, Epoch: {1:4d}, Validation error: {2:.5f}%{3}".format(
            time, epoch, validation_error * 100.0,
            ", Testing error: {0:.5f}%".format(testing_error * 100.0) if testing_error else ""))

    def setup_base_path():
        base_path_name = 'mnist_network_{}_layers_{}_activation_{}_learning_{}_minibatches{}{}{}'.format(
            '-'.join(args.hidden_layers),
            args.hidden_function,
            args.learning_rate,
            args.minibatch_size,
            '_{}_L1'.format(args.L1) if args.L1 else '',
            '_{}_L2'.format(args.L2) if args.L2 else '',
            '_{}_dropout'.format(args.dropout) if args.dropout else '')

        run_index = 1

        while True:
            base_path = os.path.join(args.output_directory, base_path_name, str(run_index))

            if os.path.isdir(base_path):
                run_index += 1
            else:
                break

        os.makedirs(base_path)

        return base_path

    parser = argparse.ArgumentParser()
    parser.add_argument('--L1', type=float)
    parser.add_argument('--L2', type=float)
    parser.add_argument('--dropout', type=float)
    parser.add_argument('--hidden_function', default='relu')
    parser.add_argument('--hidden_layers', nargs='*')
    parser.add_argument('--learning_rate', type=float, default=0.005)
    parser.add_argument('--max_epochs', type=int)
    parser.add_argument('--max_time', type=int)
    parser.add_argument('--min_epochs', type=int, default=10)
    parser.add_argument('--minibatch_size', type=int, default=20)
    parser.add_argument('--validation_ratio', type=float, default=0.1)
    parser.add_argument('--output_directory', default='data')
    args = parser.parse_args()

    base_path = setup_base_path()

    layer_sizes = [28 * 28] + list(map(int, args.hidden_layers or [])) + [10]

    print("Loading dataset 'training' from file...")
    flat_training_data, flat_training_labels = mnist_basics.load_all_flat_cases('training')

    print("Loading dataset 'testing' from file...")
    flat_testing_data, flat_testing_labels   = mnist_basics.load_all_flat_cases('testing')

    print("Creating shared Theano dataset variables...")
    training_dataset, validation_dataset, testing_dataset = build_theano_datasets(
        flat_training_data, flat_training_labels,
        flat_testing_data, flat_testing_labels,
        args.validation_ratio)

    minibatch_index = T.lscalar()
    x               = T.matrix('x')
    y               = T.ivector('y')

    activation_functions = { "relu": theano.tensor.nnet.relu }

    network = vi.theano.Network(
        x, layer_sizes, activation_functions[args.hidden_function], args.dropout, args.L1, args.L2)

    training_minibatch_count   = math.ceil(training_dataset.size   / args.minibatch_size)
    validation_minibatch_count = math.ceil(validation_dataset.size / args.minibatch_size)
    testing_minibatch_count    = math.ceil(testing_dataset.size    / args.minibatch_size)

    training_function, validation_function, testing_function = build_theano_functions(
        network, x, y, minibatch_index, args.minibatch_size, args.learning_rate,
        training_dataset, validation_dataset, testing_dataset)

    print("Starting stochastic gradient descent. learning_rate={0} min_epochs={1} max_epochs={2} max_time={3}".format(
        args.learning_rate, args.min_epochs, args.max_epochs, args.max_time))

    training_time, training_epochs, training_best_validation_error, testing_error = \
        vi.theano.stochastic_gradient_descent(
            training_function,
            training_minibatch_count,
            validation_function,
            validation_minibatch_count,
            testing_function,
            testing_minibatch_count,
            learning_rate=args.learning_rate,
            min_epochs=args.min_epochs,
            max_epochs=args.max_epochs,
            max_time=args.max_time,
            epoch_status_function=epoch_status_function)

    print(("Training completed after {:.2f} seconds. {} epochs at {:.2f} epochs / second." +
           "Best validation error: {:.5f}%, Testing error: {:.5f}%").format(
        training_time,
        training_epochs,
        training_epochs / training_time,
        training_best_validation_error * 100.0,
        testing_error * 100.0))

if __name__ == "__main__":
    main()
