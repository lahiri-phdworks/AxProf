import sys
import os
import random
import AxProf
import random
import time
import numpy as np
from scipy.stats import bernoulli


# n : Size of the Square Matrix ForAll Variable.
configList = {'n': [2, 3, 4, 5, 6, 7, 8]}

# Axprof Specification for Frievald's algorithm
spec = '''
Input list of ( list of real );
Output real;
TIME n * n;
ACC Probability over runs [ Output == 1 ] <= 0.5
'''

runs = 100


def inputParams(config, inputNum):
    return [config['n'], runs]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    output = frievalds_runner(config['n'], data)

    endTime = time.time()
    result = {'acc': output, 'time': (endTime - startTime), 'space': 0}
    return result


def frievalds_runner(n, data):
    A = [[random.randint(1, 10000) for i in range(n)] for j in range(n)]
    B = [[random.randint(1, 10000) for i in range(n)] for j in range(n)]
    C = [[random.randint(1, 10000) for i in range(n)] for j in range(n)]

    # Randomly initialize r-vector
    # TODO : Let AxProf Set this
    r = [int(num) for num in data]

    # B x r => Br
    Br = np.dot(B, r)

    # C x r => Cr
    Cr = np.dot(C, r)

    # A x B => C
    realC = np.dot(A, B)

    # P = A x Br - Cr
    P = np.subtract(np.dot(A, Br), Cr)

    ret = 1
    for i in P:
        if i != 0:
            ret = 0

    return ret


if __name__ == '__main__':
    startTime = time.time()  # Start measuring time

    """
    configList contains the ForAlls.
    """
    AxProf.checkProperties(configList, 1, runs, AxProf.binaryVectorGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')

# ==============================================================================
