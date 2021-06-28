import sys
import os
import random
import AxProf
import random
import time
from scipy.stats import bernoulli


# n : ForAll Variable.
# k : ForAll Variable
configList = {'n': [2, 3, 4, 5, 6, 7, 8, 9],
              'k': [2, 3, 4, 5, 6, 7, 8, 9, 10]}

# Axprof Specification for Monty Hall
spec = '''
Input list of real;
Output real;
n real;
k real;
TIME n;
ACC Probability over runs [ Output == 1 ] > 0.5
'''


random_runs = 10
random_input_samples = 1


def inputParams(config, inputNum):
    return [config['n'], 1, 100000]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    # Send a randomly intialized array of size "n".
    # print(data)
    output = reservoir_sampling_runner(
        [int(elem) for elem in data], config['n'], config['k'])

    endTime = time.time()
    result = {'acc': 1, 'time': (endTime - startTime), 'space': 0}
    return result


def reservoir_sampling_runner(arr, n, k):
    sample = [0] * k

    i = k
    while i < n:
        # TODO : Can we get this from AxProf
        # j is a make_pse_symbolic()
        j = random.randint(0, i)
        if j < k:
            sample[j] = arr[i]
        i = i + 1

    ret = 0
    i = 0
    while i < k:
        if arr[0] == sample[i]:
            ret = 1
        i = i + 1

    return ret


if __name__ == '__main__':
    startTime = time.time()  # Start measuring time

    """
    For different ForAll Arrays and given "n" & "k" from the configuration list.
    We run AxProf in which k is randonly sampled. 
    We need to send an array where j is sampled from [0, 1]

    configList contains the ForAlls.
    """
    AxProf.checkProperties(configList, random_runs, random_input_samples, AxProf.distinctIntegerGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')

# ==============================================================================
