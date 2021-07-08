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
configList = {'n': [2, 3, 4, 5, 6]}

# Axprof Specification for Frievald's algorithm
spec = '''
Input real;
Output real;
retProb real;
k real;
TIME n * n;
ACC Probability over runs [ Output == 1 ] <= retProb(Input)
'''

runs_per_input = 50
num_input_samples = 21

forAllInputArrays = []


def retProb(k):
    return 0.5 ** int(k[0])


def inputParams(config, inputNum):
    return [1, 1, 10]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    output = frievalds_k(
        int(config['n']), int(data[0]))

    endTime = time.time()
    result = {'acc': output, 'time': (
        endTime - startTime), 'space': 0, 'random input': {
            'k': int(data[0]),  'correct_prob': 0.5 ** int(data[0])
    }}

    # pprint(result)
    return result


def frievalds_runner(n):
    # forAllInputArrays = for_all_inputs[forall_setting_index]
    # A = forAllInputArrays[n - 2][0]
    # B = forAllInputArrays[n - 2][1]
    # C = forAllInputArrays[n - 2][2]

    # Randomly initialize r-vector
    # TODO : r ==> Let AxProf Set this

    A = [[random.randint(0, 255) for k in range(n)]
         for m in range(n)]
    B = [[random.randint(0, 255) for k in range(n)]
         for m in range(n)]
    C = [[random.randint(0, 255) for k in range(n)]
         for m in range(n)]

    r = [random.choice([0, 1]) for _ in range(n)]

    # B x r => Br
    Br = np.dot(B, r)

    # A x B x r => ABr
    ABr = np.dot(A, Br)

    # A x B => C
    realC = np.dot(A, B)

    # C x r => Cr
    Cr = np.dot(C, r)

    # res = A x Br - Cr
    res = np.subtract(ABr, Cr)

    if not all(v == 0 for v in res):
        return False
    return True


def frievalds_k(n, k):
    for _ in range(k):
        if (frievalds_runner(n) == False):
            return 0
    return 1


if __name__ == '__main__':

    # for_all_inputs = []
    # for j in configList['forall_setting']:
    #     single_forall_input = []
    #     for i in configList['n']:
    #         forAllObj = {}
    #         A = [[random.randint(0, 255) for k in range(i)]
    #              for m in range(i)]
    #         B = [[random.randint(0, 255) for k in range(i)]
    #              for m in range(i)]
    #         C = [[random.randint(0, 255) for k in range(i)]
    #              for m in range(i)]
    #         single_forall_input.append([A, B, C])
    #     for_all_inputs.append(single_forall_input)

    """
    For Each of the ForAll inputs, run AxProf "runs_per_input" times,
    each time with a different random setting.
    """

    startTime = time.time()  # Start measuring time
    """
    configList contains the ForAll setting for "n" [SIZE of Matrix].
    """
    AxProf.checkProperties(configList, runs_per_input, num_input_samples, AxProf.distinctIntegerGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(
        f'Total time required for checking : {endTime - startTime} seconds.')

# ==============================================================================
