import enum
import numpy
import timeit

def stochastic_gradient_descent(
    training_function,
    training_minibatch_count,
    testing_function,
    testing_minibatch_count,
    learning_rate,
    epochs,
    max_time=None,
    epoch_improvement_multiplier = 1.4,
    epoch_improvement_threshold = 0.995,
    epoch_status_function=None):

    best_testing_error = numpy.inf

    epoch      = 0
    start_time = timeit.default_timer()
    start_time = timeit.default_timer() # Hack workaround to initialize start_time properly

    while epoch < epochs:
        now = timeit.default_timer()

        if max_time and now - start_time >= max_time:
            break

        epoch = epoch + 1

        average_loss  = numpy.mean(list(training_function(minibatch_index) for minibatch_index in range(training_minibatch_count)))
        testing_error = numpy.mean(list(testing_function(i) for i in range(testing_minibatch_count)))

        if epoch_status_function:
            is_best = testing_error < best_testing_error
            epoch_status_function(now, epoch, average_loss, testing_error, is_best)

    end_time = timeit.default_timer()

    return (end_time - start_time, epoch, testing_error)
