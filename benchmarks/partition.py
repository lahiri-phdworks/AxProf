import sys
import os
import random
import AxProf
import random
import time
from scipy.stats import bernoulli


# n : Array Size ForAll Variable.
configList = {'n': [2, 3, 4, 5, 6, 7, 8], 'r': [1]}

# Axprof Specification for QuickSort Partitioning Algorithm.
spec = '''
Input list of real;
Output real;
n real;
TIME n;
ACC Expectation over runs [Output] == n/2
'''

random_runs = 1
random_input_samples = 1


def inputParams(config, inputNum):
    return [config['r'], 0, config['n']]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    output = partition_runner(config['n'], data)

    endTime = time.time()
    result = {'acc': output, 'time': (endTime - startTime), 'space': 0}
    return result


def partition_runner(arr, index):
    left_count = 0
    right_count = 0

    pivot = arr[index]

    for j in arr:
        if j < pivot:
            left_count += 1
        else:
            right_count += 1

    if left_count < (right_count - 1):
        outcome = (right_count - 1)
    else:
        outcome = left_count

    # We need E[outcome]
    return outcome


if __name__ == '__main__':
    startTime = time.time()  # Start measuring time

    """
    We specify that we need to run each coin-flipping session, 1000 times.
    The number of coins flipped in each session is equal to the numbers
    listed in the configList defined above.

    configList contains the ForAlls.
    """
    AxProf.checkProperties(configList, random_runs, random_input_samples, AxProf.distinctIntegerGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')

# ==============================================================================
