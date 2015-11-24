#!/usr/bin/python

import argparse
import numpy
import os

def get_datasets(base_path):
    return [ item for item in os.listdir(args.base_path) \
             if os.path.isdir(os.path.join(args.base_path, item)) ]

parser = argparse.ArgumentParser()
parser.add_argument('--base_path', default='../data')
args = parser.parse_args()

for dataset in get_datasets(args.base_path):
    error_values = []
    for item in os.listdir(os.path.join(args.base_path, dataset)):
        if os.path.isdir(os.path.join(args.base_path, dataset, item)):
            with open(os.path.join(args.base_path, dataset, item, 'error.txt')) as error_file:
                error_values.append(float(error_file.readlines()[-1].split()[2]))

    print('{} has mean {} std dev {}'.format(dataset, numpy.mean(error_values), numpy.std(error_values)))
