import vi.theano

import functools
import itertools
import operator
import random
import theano
import theano.tensor as T

class Network(object):
    def __init__(self,
                 inputs,
                 layer_sizes,
                 hidden_activation_function,
                 dropout_factor=None,
                 L1_regularization_factor=None,
                 L2_regularization_factor=None):

        self.inputs                   = inputs
        self.layer_sizes              = layer_sizes
        self.dropout_factor           = dropout_factor
        self.L1_regularization_factor = L1_regularization_factor
        self.L2_regularization_factor = L2_regularization_factor

        self.layers = []

        srng = T.shared_randomstreams.RandomStreams(seed=random.randint(0, 2 ** 30))

        training_inputs = testing_inputs = inputs

        for layer_index in range(1, len(layer_sizes)):
            is_output_layer = layer_index == len(layer_sizes) - 1

            activation_function = T.nnet.softmax if is_output_layer \
                                  else hidden_activation_function

            layer = vi.theano.Layer(
                srng,
                training_inputs,
                testing_inputs,
                layer_sizes,
                layer_index,
                activation_function,
                dropout_factor)

            self.layers.append(layer)

            training_inputs = layer.training_outputs
            testing_inputs  = layer.testing_outputs

    def classify(self):
        return T.argmax(self.layers[-1].testing_outputs, axis=1)

    def errors(self, y):
        return T.mean(T.neq(self.classify(), y))

    def loss_function(self, y):
        loss = -T.mean(T.log(self.layers[-1].training_outputs)[T.arange(y.shape[0]), y])

        if self.L1_regularization_factor:
            L1_regularization_terms = functools.reduce(
                operator.add, (abs(layer.weights).sum() for layer in self.layers))

            loss += self.L1_regularization_factor * L1_regularization_terms

        if self.L2_regularization_factor:
            L2_regularization_terms = functools.reduce(
                operator.add, ((layer.weights ** 2).sum() for layer in self.layers))

            loss += self.L2_regularization_factor * L2_regularization_terms

        return loss

    def parameters(self):
        return list(itertools.chain.from_iterable(layer.parameters for layer in self.layers))
