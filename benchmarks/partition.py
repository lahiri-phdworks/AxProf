import sys
import os
import random
import AxProf
import random
import time
from scipy.stats import bernoulli


# n : Array Size ForAll Variable.
configList = {'n': [1, 2, 3, 4, 5, 6, 7, 8]}

# Axprof Specification for QuickSort Partitioning Algorithm.
spec = '''
Input list of real;
Output real;
n real;
TIME n;
ACC Expectation over runs [Output] == ???
'''


def inputParams(config, inputNum):
    return [config['n'], 1, 100000]


def runner():
    pass


def partition_runner():
    pass


if __name__ == '__main__':
    startTime = time.time()  # Start measuring time

    """
    We specify that we need to run each coin-flipping session, 1000 times.
    The number of coins flipped in each session is equal to the numbers
    listed in the configList defined above.

    configList contains the ForAlls.
    """
    AxProf.checkProperties(configList, 50, 1, AxProf.distinctIntegerGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')

# ==============================================================================
