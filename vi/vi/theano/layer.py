import numpy
import theano

class Layer():
    def __init__(self, srng,
                 training_inputs, testing_inputs,
                 layer_sizes, layer_index,
                 activation_function, dropout_factor):

        self.training_inputs      = training_inputs
        self.testing_inputs       = testing_inputs
        self.layer_sizes          = layer_sizes
        self.layer_index          = layer_index
        self.activation_function  = activation_function
        self.dropout_factor       = dropout_factor

        self.input_size = layer_sizes[layer_index - 1]
        self.layer_size = layer_sizes[layer_index]

        if activation_function is theano.tensor.nnet.relu:
            # Initialize weights according to "Delving Deep into Rectifiers:
            # Surpassing Human-Level Performance on ImageNet Classification":
            weight_values = numpy.asarray(
                numpy.random.randn(self.input_size, self.layer_size) * numpy.sqrt(2.0 / self.input_size),
                dtype=theano.config.floatX)
        else:
            weight_values = numpy.asarray(
                numpy.random.uniform(
                    low=-numpy.sqrt(6.0 / (self.input_size + self.layer_size)),
                    high=numpy.sqrt(6.0 / (self.input_size + self.layer_size)),
                    size=(self.input_size, self.layer_size)),
                dtype=theano.config.floatX)

            if activation_function is theano.tensor.nnet.sigmoid:
                weight_values *= 4

        self.bias = theano.shared(
            value=numpy.zeros((self.layer_size,), dtype=theano.config.floatX),
            borrow=True)

        self.weights    = theano.shared(value=weight_values, borrow=True)
        self.parameters = [self.bias, self.weights]

        self.testing_outputs = self.activation_function(
            theano.tensor.dot(self.testing_inputs, self.weights) + self.bias)

        if dropout_factor:
            # Inverted dropout. Does not require scaling at testing time.
            mask = (srng.uniform(size=self.training_inputs.shape) < self.dropout_factor) / self.dropout_factor
            self.training_inputs = self.training_inputs * mask

            self.training_outputs = self.activation_function(
                theano.tensor.dot(self.training_inputs, self.weights) + self.bias)
        else:
            self.training_outputs = self.testing_outputs
