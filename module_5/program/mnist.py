#!/usr/bin/python3

import argparse
import collections
import itertools
import math
import numpy
import os
import pickle
import random
import sys
import theano
import theano.tensor as T
import time

sys.path.append('../mnist/basics')
import mnist_basics
sys.path.append('../../vi')
import vi.theano

def build_theano_dataset(flat_data, flat_labels):
    data_array   = numpy.asarray(flat_data, dtype=theano.config.floatX)
    data_array  /= 255.0 # Scale to [0-1]
    labels_array = numpy.asarray(flat_labels, dtype=theano.config.floatX)

    shared_data   = theano.shared(data_array, borrow=True)
    shared_labels = T.cast(theano.shared(labels_array, borrow=True), 'int32')

    return vi.theano.TheanoDataSet(shared_data, shared_labels, len(flat_data))

def build_theano_functions(
    network, x, y, minibatch_index, minibatch_size, learning_rate,
    training_dataset, testing_dataset):

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

    return training_function, testing_function

# http://stackoverflow.com/a/11325249
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()

class Ann(object):
    def __init__(self, predict_function, minibatch_size=1):
        self.predict_function = predict_function
        self.minibatch_size   = minibatch_size

    def blind_test(self, images):
        minibatch_count = int(math.ceil(len(images) / self.minibatch_size))
        return list(itertools.chain(list(self.predict_function(images[i * self.minibatch_size : (i + 1) * self.minibatch_size]))
                                    for i in range(minibatch_count)))

def main():
    def epoch_status_function(time, epoch, average_loss, testing_error, is_best):
        if is_best:
            with open(os.path.join(base_path, 'model.pkl'), 'wb') as model_file:
                pickle.dump(network, model_file)

        with open(os.path.join(base_path, 'loss.txt'), 'at') as error_file:
            print('{} {:.4f} {:.10f}'.format(epoch, time, average_loss), file=error_file)

        with open(os.path.join(base_path, 'error.txt'), 'at') as error_file:
            print('{} {:.4f} {:.10f}'.format(epoch, time, testing_error * 100.0), file=error_file)

        print("Time: {:7.2f} sec, Epoch: {:4d}, Testing error: {:.5f}%".format(
            time, epoch, testing_error * 100.0))

    def setup_base_path(runs):
        def format_float(f):
            return '{:f}'.format(f).rstrip('0').rstrip('.')

        base_path = os.path.join(args.output_directory,
            'mnist_network_{}_layers_{}_activation_{}_learning_{}_minibatches{}{}{}'.format(
                '-'.join(args.hidden_layers),
                args.hidden_function,
                format_float(args.learning_rate),
                args.minibatch_size,
                ('_' + format_float(args.L1) + '_L1') if args.L1 else '',
                ('_' + format_float(args.L2) + '_L2') if args.L2 else '',
                ('_' + format_float(args.dropout) + '_dropout') if args.dropout else ''))

        if runs:
            run_index = 1

            while True:
                base_path_run = os.path.join(base_path, str(run_index))

                if os.path.isdir(base_path_run):
                    run_index += 1
                else:
                    base_path = base_path_run
                    break

        if not os.path.isdir(base_path):
            os.makedirs(base_path)

        existing_files = [ f for f in os.listdir(base_path) ]
        for existing_file in existing_files:
            try:
                os.remove(existing_file)
            except:
                pass

        return base_path

    parser = argparse.ArgumentParser()
    parser.add_argument('--L1', type=float)
    parser.add_argument('--L2', type=float)
    parser.add_argument('--R', type=int)
    parser.add_argument('--data')
    parser.add_argument('--dropout', type=float)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--hidden_function', default='relu')
    parser.add_argument('--hidden_layers', nargs='*')
    parser.add_argument('--learning_rate', type=float, default=0.005)
    parser.add_argument('--major_demo', action='store_true')
    parser.add_argument('--max_time', type=int)
    parser.add_argument('--minibatch_size', type=int, default=40)
    parser.add_argument('--minor_demo', action='store_true')
    parser.add_argument('--model')
    parser.add_argument('--output_directory', default='../data')
    parser.add_argument('--runs', action='store_true')
    parser.add_argument('--seed', type=int)
    parser.add_argument('--training_ratio', type=float)
    args = parser.parse_args()

    print(args)

    if args.seed:
        random.seed(args.seed)
        numpy.random.seed(random.randint(0, 2 ** 30))

    if (args.major_demo or args.minor_demo) and not args.model:
        print("No model file provided.", file=sys.stderr)
        sys.exit(-1)

    if args.model:
        network = pickle.load(open(args.model, 'rb'))

        predict_function = theano.function(
            inputs=[network.inputs],
            outputs=network.classify())

        if args.major_demo:
            if not args.R:
                print("No R parameter provided.", file=sys.stderr)
                sys.exit(-1)

            ann = Ann(predict_function)
            d   = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../mnist/basics/')
            print('r = {} d = {}'.format(args.R, d))

            mnist_basics.major_demo(ann, args.R, d)
        elif args.minor_demo:
            mnist_basics.minor_demo(Ann(predict_function, args.minibatch_size))
        elif args.data:
            dataset, labelset = pickle.load(open(args.data, 'rb'))

            total = len(dataset)
            correct = sum(predict_function(dataset[i:i+1])[0] == labelset[i:i+1][0] for i in range(len(dataset)))

            print("{}/{} ({:.2f}%)".format(correct, total, 100.0 * correct / total))
        else:
            print("No data file provided.", file=sys.stderr)
            sys.exit(-1)
    else:
        base_path = setup_base_path(args.runs)

        with open(os.path.join(base_path, 'log.txt'), 'at') as log_file:
            temp_stdout = sys.stdout
            sys.stdout  = Tee(sys.stdout, log_file)

            layer_sizes = [28 * 28] + list(map(int, args.hidden_layers or [])) + [10]

            print("Loading dataset 'training' from file...")
            flat_training_data, flat_training_labels = mnist_basics.load_all_flat_cases('training', dir='../mnist/basics/')

            print("Loading dataset 'testing' from file...")
            flat_testing_data, flat_testing_labels = mnist_basics.load_all_flat_cases('testing', dir='../mnist/basics/')

            print("Creating shared Theano dataset variables...")

            num_training_examples = int(math.ceil(args.training_ratio * len(flat_training_data))) if args.training_ratio else len(flat_training_data)

            training_dataset = build_theano_dataset(flat_training_data[:num_training_examples], flat_training_labels[:num_training_examples])
            testing_dataset  = build_theano_dataset(flat_testing_data, flat_testing_labels)

            minibatch_index = T.lscalar()
            x               = T.matrix('x')
            y               = T.ivector('y')

            activation_functions = { "relu": theano.tensor.nnet.relu, "sigmoid": theano.tensor.nnet.sigmoid, "tanh": theano.tensor.tanh }

            network = vi.theano.Network(
                x, layer_sizes, activation_functions[args.hidden_function], args.dropout, args.L1, args.L2)

            training_minibatch_count = int(math.ceil(training_dataset.size / args.minibatch_size))
            testing_minibatch_count  = int(math.ceil(testing_dataset.size  / args.minibatch_size))

            training_function, testing_function = build_theano_functions(
                network, x, y, minibatch_index, args.minibatch_size, args.learning_rate,
                training_dataset, testing_dataset)

            print("Starting stochastic gradient descent. num_training_examples={}".format(
                num_training_examples, args.learning_rate, args.epochs, args.max_time))

            training_time, training_epochs, testing_error = \
                vi.theano.stochastic_gradient_descent(
                    training_function,
                    training_minibatch_count,
                    testing_function,
                    testing_minibatch_count,
                    learning_rate=args.learning_rate,
                    epochs=args.epochs,
                    max_time=args.max_time,
                    epoch_status_function=epoch_status_function)

            print(("Training completed after {:.2f} seconds. {} epochs at {:.2f} epochs / second. " +
                   "Testing error: {:.5f}%").format(
                training_time,
                training_epochs,
                training_epochs / training_time,
                testing_error * 100.0))

            time.sleep(1)
            sys.stdout.flush()
            sys.stdout = temp_stdout

if __name__ == "__main__":
    main()
