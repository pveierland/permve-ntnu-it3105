#!/bin/bash

epochs=250
output_directory=magic

default_layer_size=512
default_learning_rate=0.08
default_minibatch_size=20
default_L2=0.0001

for i in {1..20}
do
    python -u ../program/mnist.py --hidden_layers ${default_layer_size} --epochs ${epochs} --minibatch_size ${default_minibatch_size} --output_directory ${output_directory} --learning_rate ${default_learning_rate} --hidden_function sigmoid --runs
done

for i in {1..20}
do
    python -u ../program/mnist.py --hidden_layers ${default_layer_size} --epochs ${epochs} --minibatch_size ${default_minibatch_size} --output_directory ${output_directory} --learning_rate ${default_learning_rate} --hidden_function tanh --runs
done

for i in {1..20}
do
    python -u ../program/mnist.py --hidden_layers ${default_layer_size} --epochs ${epochs} --minibatch_size ${default_minibatch_size} --output_directory ${output_directory} --learning_rate ${default_learning_rate} --hidden_function relu --runs
done

for i in {1..20}
do
    python -u ../program/mnist.py --hidden_layers ${default_layer_size} --epochs ${epochs} --minibatch_size ${default_minibatch_size} --output_directory ${output_directory} --learning_rate ${default_learning_rate} --hidden_function relu --L2 0.00005 --runs
done

for i in {1..20}
do
    python -u ../program/mnist.py --hidden_layers ${default_layer_size} --epochs ${epochs} --minibatch_size ${default_minibatch_size} --output_directory ${output_directory} --learning_rate ${default_learning_rate} --hidden_function relu --L2 0.0001 --runs
done

for i in {1..20}
do
    python -u ../program/mnist.py --hidden_layers ${default_layer_size} --epochs ${epochs} --minibatch_size ${default_minibatch_size} --output_directory ${output_directory} --learning_rate ${default_learning_rate} --hidden_function relu --L2 0.0005 --runs
done

for i in {1..20}
do
    python -u ../program/mnist.py --hidden_layers ${default_layer_size} --epochs ${epochs} --minibatch_size ${default_minibatch_size} --output_directory ${output_directory} --learning_rate ${default_learning_rate} --hidden_function relu --dropout 0.8 --runs
done

for i in {1..20}
do
    python -u ../program/mnist.py --hidden_layers ${default_layer_size} --epochs ${epochs} --minibatch_size ${default_minibatch_size} --output_directory ${output_directory} --learning_rate ${default_learning_rate} --hidden_function relu --dropout 0.5 --runs
done
