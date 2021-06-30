import sys
import os
import random
import AxProf
import random
import time
import math
from scipy.stats import bernoulli
from IPython.lib.pretty import pprint

# This is fixed pivot quicksort instead of being randomized quicksort.
# n : Array Size ForAll Variable.
configList = {'n': [2, 3, 4, 5, 6, 7, 8, 9, 10], 'forall_setting': range(150)}

# Axprof Specification for QuickSort Algorithm.
spec = '''
Input list of real;
Output real;
n real;
math.log real;
TIME n * n;
ACC Expectation over inputs [ Output ] <= 1.2 * n * math.log(n, 2)
'''

runs_per_input = 1
num_input_samples = 2
quicksort_arrays = []
compare_count = 0


def inputParams(config, inputNum):
    return [config['n'], 0, config['n'] - 1]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    global compare_count
    compare_count = 0

    output = quicksort_runner(
        quicksort_arrays[config['n'] - 2][config['forall_setting']], 0, config['n'] - 1)

    endTime = time.time()
    result = {'acc': output, 'time': (endTime - startTime), 'space': 0, 'random input': {
        'forall_array': quicksort_arrays[config['n'] - 2][config['forall_setting']], 'forall_n': config['n'], 'compare': compare_count
    }}

    pprint(result)
    return result


def partition(arr, start, end):
    i = start - 1

    # This "index" must choosen by AxProf
    # in case of randomized quicksort
    pivot = arr[end]

    compare = 0
    for j in range(start, end):
        if arr[j] <= pivot:
            compare = compare + 1
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[end] = arr[end], arr[i + 1]
    return i + 1, compare


def quicksort_runner(arr, start, end):
    compare = 0
    if start < end:
        pivot_index, compare = partition(arr, start, end)

        # Divide and conquer !
        quicksort_runner(arr, start, pivot_index - 1)
        quicksort_runner(arr, pivot_index + 1, end)

    global compare_count
    compare_count = compare + compare_count
    return compare_count


if __name__ == '__main__':
    for sizes in configList['n']:
        forall_arrays = []
        for index in configList['forall_setting']:
            forall_inputs = []
            for i in range(sizes):
                forall_inputs.append(random.randint(-15000, 15000))
            forall_arrays.append(forall_inputs)
        quicksort_arrays.append(forall_arrays)

    startTime = time.time()  # Start measuring time

    """
    We specify that we need to run each coin-flipping session, 1000 times.
    The number of coins flipped in each session is equal to the numbers
    listed in the configList defined above. 

    configList contains the ForAlls.
    """
    AxProf.checkProperties(configList, runs_per_input, num_input_samples, AxProf.distinctIntegerGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')


# ==============================================================================
