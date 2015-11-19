import numpy
import theano

class Layer():
    def __init__(self, srng,
                 training_inputs, testing_inputs,
                 input_size, layer_size, activation_function, dropout_factor):

        self.training_inputs     = training_inputs
        self.testing_inputs      = testing_inputs
        self.input_size          = input_size
        self.layer_size          = layer_size
        self.activation_function = activation_function
        self.dropout_factor      = dropout_factor

        if activation_function is theano.tensor.nnet.relu:
            # Initialize weights according to "Delving Deep into Rectifiers:
            # Surpassing Human-Level Performance on ImageNet Classification":
            weight_values = numpy.asarray(
                numpy.random.randn(input_size, layer_size) * numpy.sqrt(2.0 / input_size),
                dtype=theano.config.floatX)
        else:
            weight_values = numpy.zeros((input_size, layer_size), dtype=theano.config.floatX)

        self.bias = theano.shared(
            value=numpy.zeros((layer_size,), dtype=theano.config.floatX),
            borrow=True)

        self.weights    = theano.shared(value=weight_values, borrow=True)
        self.parameters = [self.bias, self.weights]

        self.testing_outputs = self.activation_function(
            theano.tensor.dot(self.testing_inputs, self.weights) + self.bias)

        if dropout_factor:
            mask = (srng.uniform(size=training_inputs.shape) < self.dropout_factor) / self.dropout_factor
            training_inputs = training_inputs * mask

            self.training_outputs = self.activation_function(
                theano.tensor.dot(self.training_inputs, self.weights) + self.bias)
        else:
            self.training_outputs = self.testing_outputs
