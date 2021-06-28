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
configList = {'n': [2, 3, 4, 5]}

# Axprof Specification for Frievald's algorithm
spec = '''
Input list of ( list of real );
Output real;
TIME n * n;
ACC Probability over runs [ Output == 1 ] < 0.5
'''

random_runs = 1
num_foralls = 1
random_input_samples = 0

forAllInputArrays = []


def inputParams(config, inputNum):
    return [config['n'], random_runs]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    output = frievalds_runner(config['n'], data)

    endTime = time.time()
    result = {'acc': output, 'time': (
        endTime - startTime), 'space': 0, 'random input': data}
    print(f"Results for Random Input : {result}")
    return result


def frievalds_runner(n, data):
    A = forAllInputArrays[n - 2][0]
    B = forAllInputArrays[n - 2][1]
    C = forAllInputArrays[n - 2][2]

    # Randomly initialize r-vector
    # TODO : Let AxProf Set this
    r = [int(num) for num in data]

    # B x r => Br
    Br = np.dot(B, r)

    # A x B x r => ABr
    ABr = np.dot(A, Br)

    # C x r => Cr
    Cr = np.dot(C, r)

    # A x B => C
    # realC = np.dot(A, B)

    # res = A x Br - Cr
    res = np.subtract(ABr, Cr)

    ret = 1

    for i in res:
        if i != 0:
            ret = 0

    return 1


if __name__ == '__main__':

    for_all_inputs = []
    for j in range(num_foralls):
        single_forall_input = []
        for i in configList['n']:
            forAllObj = {}
            A = [[random.randint(1, 10000) for k in range(i)]
                 for m in range(i)]
            B = [[random.randint(1, 10000) for k in range(i)]
                 for m in range(i)]
            C = [[random.randint(1, 10000) for k in range(i)]
                 for m in range(i)]
            single_forall_input.append([A, B, C])
        for_all_inputs.append(single_forall_input)
    """
        For Each of the ForAll inputs, run AxProf "random_runs" times, 
        each time with a different random setting.
    """

    for forall_setting in range(len(for_all_inputs)):
        forAllInputArrays = for_all_inputs[forall_setting]
        startTime = time.time()  # Start measuring time
        """
        configList contains the ForAll setting for "n" [SIZE of Matrix].
        """
        AxProf.checkProperties(configList, random_runs, random_input_samples, AxProf.binaryVectorGenerator,
                               inputParams, runner, spec=spec)
        endTime = time.time()  # Stop measuring time
        print(
            f'Total time required for checking : {endTime - startTime} seconds.')

# ==============================================================================
