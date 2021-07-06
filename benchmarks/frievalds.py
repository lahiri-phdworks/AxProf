import sys
import os
import random
import AxProf
import random
import time
import numpy as np
from scipy.stats import bernoulli
from IPython.lib.pretty import pprint

# n : Size of the Square Matrix ForAll Variable.
configList = {'forall_setting': range(100), 'n': [2, 3, 4, 5, 6]}

# Axprof Specification for Frievald's algorithm
spec = '''
Input list of ( list of real );
Output real;
TIME n * n;
ACC Probability over inputs [ Output == 1 ] >= 0.5
'''

runs_per_input = 1
num_input_samples = 100

forAllInputArrays = []


def inputParams(config, inputNum):
    return [config['n']]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    output = frievalds_runner(config['forall_setting'], config['n'], [
                              int(r) for r in data])

    endTime = time.time()
    result = {'acc': output, 'time': (
        endTime - startTime), 'space': 0, 'random input': {
            'forall_setting_index': config['forall_setting'], 'pse_r': [int(r) for r in data]
    }}

    pprint(result)
    return result


def frievalds_runner(forall_setting_index, n, r):
    forAllInputArrays = for_all_inputs[forall_setting_index]
    A = forAllInputArrays[n - 2][0]
    B = forAllInputArrays[n - 2][1]
    C = forAllInputArrays[n - 2][2]

    # Randomly initialize r-vector
    # TODO : r ==> Let AxProf Set this

    # B x r => Br
    Br = np.dot(B, r)

    # A x B x r => ABr
    ABr = np.dot(A, Br)

    # C x r => Cr
    Cr = np.dot(C, r)

    # A x B => C
    realC = np.dot(A, B)

    # res = A x Br - Cr
    res = np.subtract(ABr, Cr)

    ret = 1

    for i in res:
        if i != 0:
            ret = 0

    return ret


if __name__ == '__main__':

    for_all_inputs = []
    for j in configList['forall_setting']:
        single_forall_input = []
        for i in configList['n']:
            forAllObj = {}
            A = [[random.randint(0, 255) for k in range(i)]
                 for m in range(i)]
            B = [[random.randint(0, 255) for k in range(i)]
                 for m in range(i)]
            C = [[random.randint(0, 255) for k in range(i)]
                 for m in range(i)]
            single_forall_input.append([A, B, C])
        for_all_inputs.append(single_forall_input)

    """
    For Each of the ForAll inputs, run AxProf "runs_per_input" times, 
    each time with a different random setting.
    """

    startTime = time.time()  # Start measuring time
    """
    configList contains the ForAll setting for "n" [SIZE of Matrix].
    """
    AxProf.checkProperties(configList, runs_per_input, num_input_samples, AxProf.binaryVectorGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(
        f'Total time required for checking : {endTime - startTime} seconds.')

# ==============================================================================
