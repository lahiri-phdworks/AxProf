import sys
import os
import random
import AxProf
import random
import time
import math
from scipy.stats import bernoulli
from subprocess import run, CalledProcessError
from IPython.lib.pretty import pprint

# Randomized Quick Sort
# n : Array Size ForAll Variable.
configList = {'n': [5]}


# Axprof Specification for Randomized Quick Sort Algorithm.
spec = '''
Input list of real;
Output real;
math.log real;
ACC Expectation over inputs [ Output ] > 0.55 * n * math.log(n, 2) 
'''

runs_per_input = 10
num_input_samples = 100  # Number of arrays to generate.


# Randomized Quick Sort Specific
quicksort_arrays = []
compare_count = 0


def execute(inFile, outfile, errFile):
    try:
        output = run(
            f"bin/quicksort < {inFile} > {outfile} 2> {errFile}",
            shell=True,
            capture_output=False,
            text=True,
        )
    except CalledProcessError as err:
        print(f"Execute Error : {err}")
    else:
        output = run(["cat", f"{outfile}"], capture_output=True)
        return int(output.stdout)


def inputParams(config, inputNum):
    return [config['n'], 0, 255]


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
    arr = [int(x) for x in data]
    # Error (Interestingly, the error is not detected for large N)
    output = quicksort_runner(arr)
    # print(arr == sorted(arr))
    # sys.exit("[Post Condition Failure] : Array not sorted !")

    endTime = time.time()
    result = {'acc': output, 'time': (endTime - startTime), 'space': 0, 'input': {
        'size': config['n'], 'expected': 1.36 * config['n'] * math.log(config['n'])
    }}

    # 'random input': {
    #     'forall_array': quicksort_arrays[config['n'] - 2][config['forall_setting']],
    #       'forall_n': config['n'], 'compare': compare_count
    # }

    # pprint(result)
    return result

# *****************************************************************


def quicksort_runner(arr):
    with open(f"tests/quicksort.txt", mode="w") as fileptr:
        for data in arr:
            fileptr.write(f"{data}\n")
    return execute(f"tests/quicksort.txt", f"tests/output.txt", f"tests/error.txt")


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
