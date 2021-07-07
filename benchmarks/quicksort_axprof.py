import sys
import os
import random
import AxProf
import random
import time
import math
from scipy.stats import bernoulli
from IPython.lib.pretty import pprint

# Randomized Quick Sort
# n : Array Size ForAll Variable.
configList = {'n': [10]}


# Axprof Specification for Randomized Quick Sort Algorithm.
spec = '''
Input list of real;
Output real;
k real;
n real;
math.factorial real;
TIME n * math.log(n, 2);
ACC Expectation over runs [ Output ] >= 0.25 * n * math.log(n, 2) 
'''

runs_per_input = 2000
num_input_samples = 100  # Number of arrays to generate.


# Randomized Quick Sort Specific
quicksort_arrays = []
compare_count = 0


def inputParams(config, inputNum):
    return [config['n'], -9999999, 9999999]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    global compare_count
    compare_count = 0

    """
    We use input from AxProf now. For each array from AxProf, 
    we run it multiple times (runs_per_input times to be precise)
    """
    output = quicksort_runner([int(x)
                              for x in data], 0, config['n'] - 2)  # Error (Interestingly, the error is not detected for large N)

    endTime = time.time()
    result = {'acc': output, 'time': output, 'space': 0, 'input': {
        'size': config['n'], 'expected': 0.5 * config['n'] * math.log(config['n'])
    }}

    # 'random input': {
    #     'forall_array': quicksort_arrays[config['n'] - 2][config['forall_setting']],
    #       'forall_n': config['n'], 'compare': compare_count
    # }

    pprint(result)
    return result

# *****************************************************************


def partition(arr, start, end):
    i = start - 1

    # This "index" must choosen by AxProf
    # in case of randomized quicksort
    pivot = arr[random.randint(start, end)]

    compare = 0
    for j in range(start, end):
        # Error : Must be "j" if used j - 1 or j + 1
        # Does not affect compare.
        if arr[j] <= pivot:
            compare = compare + 1
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[end] = arr[end], arr[i + 1]

    return i + 1, compare


def quicksort_runner(arr, start, end):
    """[summary]

    Args:
        arr (list): [Array to be sorted]
        start (int): [start index]
        end (int): [end index]

    Returns:
        [int]: [# Comparisions for sorting array between start & end]
    """
    compare = 0
    if start < end:
        pivot_index, compare = partition(arr, start, end)

        # Divide and conquer !
        quicksort_runner(arr, start, pivot_index - 1)
        quicksort_runner(arr, pivot_index + 1, end)

    global compare_count
    compare_count = compare + compare_count
    return compare_count

# *****************************************************************


if __name__ == '__main__':

    startTime = time.time()  # Start measuring time

    """
    We specify that we need to run each sorting session, say 1000 times.
    We let AxProf construct the array to be sorted by quicksort_runner()
    """
    AxProf.checkProperties(configList, runs_per_input, num_input_samples, AxProf.distinctIntegerGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')


# ==============================================================================
