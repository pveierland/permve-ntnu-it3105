import enum
import numpy
import timeit

def stochastic_gradient_descent(
    training_function,
    training_minibatch_count,
    validation_function,
    validation_minibatch_count,
    testing_function,
    testing_minibatch_count,
    learning_rate,
    min_epochs,
    max_epochs,
    max_time,
    epoch_improvement_multiplier = 1.4,
    epoch_improvement_threshold = 0.995,
    epoch_status_function=None):

    best_validation_error = numpy.inf
    current_testing_error = numpy.inf
    last_testing_error    = numpy.inf

    epoch      = 0
    start_time = timeit.default_timer()

    while (min_epochs and epoch < min_epochs) or (max_epochs and epoch < max_epochs):
        now = timeit.default_timer()

        if max_time and now - start_time >= max_time:
            break

        epoch = epoch + 1

        average_loss     = numpy.mean(list(training_function(minibatch_index) for minibatch_index in range(training_minibatch_count)))
        validation_error = numpy.mean(list(validation_function(i) for i in range(validation_minibatch_count)))

        if validation_error < best_validation_error:
            if validation_error < best_validation_error * epoch_improvement_threshold:
                min_epochs = max(min_epochs or 0, epoch * epoch_improvement_multiplier)

            best_validation_error = validation_error
            best_epoch            = epoch

            last_testing_error = current_testing_error = numpy.mean(list(testing_function(i) for i in range(testing_minibatch_count)))
        else:
            current_testing_error = None

        if epoch_status_function:
            epoch_status_function(now, epoch, average_loss, validation_error, current_testing_error)

    end_time = timeit.default_timer()

    return (end_time - start_time, epoch, best_validation_error, last_testing_error)
