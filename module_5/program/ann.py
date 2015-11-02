#!/usr/bin/python3

import numpy
import theano
import theano.tensor as T
import sys
import time

sys.path.append('../input/basics')
import mnist_basics

class colors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

num_input_nodes  = 784
num_hidden_nodes = 784
num_output_nodes = 10

learning_rate = 0.00001

weights_hidden = theano.shared(
    numpy.random.uniform(-0.1, +0.1, size=(num_input_nodes, num_hidden_nodes)))

weights_output = theano.shared(
    numpy.random.uniform(-0.1, +0.1, size=(num_hidden_nodes, num_output_nodes)))

input          = T.dvector('input')
desired_output = T.dvector('desired_output')

bias_hidden = theano.shared(numpy.random.uniform(-0.1, +0.1, size=num_hidden_nodes))
bias_output = theano.shared(numpy.random.uniform(-0.1, +0.1, size=num_output_nodes))

x1 = T.nnet.sigmoid(theano.dot(input, weights_hidden) + bias_hidden)
x2 = T.nnet.sigmoid(theano.dot(x1, weights_output) + bias_output)

error = T.sum((desired_output - x2) ** 2)

parameters = [weights_hidden, bias_hidden, weights_output, bias_output]
gradients  = theano.grad(error, parameters)

backprop_acts = [(p, p - learning_rate * g) for p, g in zip(parameters, gradients)]

predictor = theano.function([input], [x2, x1])
trainer   = theano.function([input, desired_output], error, updates=backprop_acts)

print("Infrastructure completed")

# Iterate through training examples

training_cases  = mnist_basics.gen_flat_cases()#digits=[1, 2])
training_inputs = [numpy.array(x) / 255.0 for x in training_cases[0]]

print("Done setting up training data")

training_desired_outputs = []

for n in range(10):
    desired_outputs    = numpy.zeros(10)
    desired_outputs.fill(-1.0)
    desired_outputs[n] = +1.0
    training_desired_outputs.append(desired_outputs)

print("Desired outputs lookup table built")

errors = []

import matplotlib.pyplot as plt

start_time = time.time()

for epochs in range(100):
    for training_case_id, training_input in enumerate(training_inputs):
    #    print("TRAINING INPUT = {0}".format(training_input))
    #    print("TRAINING_DESIRED_OUTPUT = {0}".format(training_desired_outputs[training_cases[1][training_case_id]]))
        desired_wtf = training_desired_outputs[training_cases[1][training_case_id]]

        e = trainer(training_input, desired_wtf)
        errors.append(e)

        #print("{0}/{1}: {2} {3}".format(training_case_id, len(training_inputs), desired_wtf, e))
    now = time.time()
    print("{0:.2f}: Completed epoch {1} e = {2}".format((now - start_time), epochs + 1, e))

    #if not epochs % 10:
    #    plt.plot(range(1, len(errors) + 1), errors)
    #    plt.show()


