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
configList = {'n': [2, 3, 4, 5, 6, 7, 8, 9, 10],
              'forall_setting': range(5000)}  # 0 .... 5000


# Setting-1 (n = 4) [4, -5, 6, 8]
# Setting-2 (n = 4) [5, 85, 6, 12]
# .... 5000 different arrays to try

# Axprof Specification for Randomized Quick Sort Algorithm.
spec = '''
Input list of real;
Output real;
n real;
math.log real;
TIME n * math.log(n, 2);
ACC Expectation over runs [ Output ] > 1.5 * n * math.log(n, 2)
'''

runs_per_input = 100
num_input_samples = 1


# Randomized Quick Sort Specific
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

    """
    We dont need to use the input from AxProf here since all 
    inputs are already provided by us in the forall arrays.
    """
    output = quicksort_runner(
        quicksort_arrays[config['n'] - 2][config['forall_setting']], 0, config['n'] - 1)

    endTime = time.time()
    result = {'acc': output, 'time': (endTime - startTime), 'space': 0}

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
    # Forall Arrays initialized
    # We supply it to runner called by AxProf
    # Input is specified by us in this case.
    for sizes in configList['n']:
        forall_arrays = []
        for index in configList['forall_setting']:
            forall_inputs = []
            for i in range(sizes):
                forall_inputs.append(random.randint(-100000, 100000))
            forall_arrays.append(forall_inputs)
        quicksort_arrays.append(forall_arrays)

    startTime = time.time()  # Start measuring time

    """
    We specify that we need to run each sorting session, say 1000 times.
    The number of coins flipped in each session is equal to the numbers
    listed in the configList defined above. 

    configList contains the ForAlls.
    """
    AxProf.checkProperties(configList, runs_per_input, num_input_samples, AxProf.distinctIntegerGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')


# ==============================================================================
