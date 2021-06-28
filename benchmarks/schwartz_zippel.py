import sys
import os
import random
import AxProf
import random
import time
from scipy.stats import bernoulli


# n : ForAll Variable.
# subset_max : ForAll Variable
configList = {'n': [2, 3, 4, 5],
              'subset_max': [11]}

# Axprof Specification for Monty Hall
spec = '''
Input list of real;
Output real;
n real;
subset_max real;
TIME n;
ACC Probability over runs [ Output != 0 ] >= n / subset_max
'''


random_runs = 1
random_input_samples = 1


def inputParams(config, inputNum):
    return [config['coins'], 1, 3]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    output = schwartz_zippel_runner(config['n'], data)

    endTime = time.time()
    result = {'acc': output, 'time': (
        endTime - startTime), 'space': 0, 'random input': data}

    print(result)
    return result


def schwartz_zippel_runner(poly, r, d):
    total = 0

    # This was value intialized in the main function.
    d = [1] * len(poly)
    for index, item in enumerate(poly):
        total += item * (r[index] ** d[index])

    return total == 0


if __name__ == '__main__':
    startTime = time.time()  # Start measuring time

    """
    We specify that we need to run each coin-flipping session, 1000 times.
    The number of coins flipped in each session is equal to the numbers
    listed in the configList defined above. 

    configList contains the ForAlls.
    """
    AxProf.checkProperties(configList, random_runs, random_input_samples, AxProf.distinctIntegerGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')

# ==============================================================================
