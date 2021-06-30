import sys
import os
import random
import AxProf
import random
import time
from scipy.stats import bernoulli
from IPython.lib.pretty import pprint

# n : ForAll Variable.
# subset_max : ForAll Variable
configList = {'n': [2, 3, 4, 5, 6],
              'subset_max': [10, 11, 12]}

polynomials = []

# Axprof Specification for Monty Hall
spec = '''
Input list of real;
Output real;
n real;
subset_max real;
TIME n;
ACC Probability over inputs [ Output != 0 ] >= n / subset_max
'''


runs_per_input = 1
num_input_samples = 500


def inputParams(config, inputNum):
    return [config['n'], 0, config['subset_max']]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    output = schwartz_zippel_runner(config['n'], [int(r) for r in data])

    endTime = time.time()
    result = {'acc': output, 'time': (
        endTime - startTime), 'space': 0, 'random input': {
            'forall_polynomial': polynomials[config['n'] - 2], 'forall_n': config['n'], 'forall_subset_max': config['subset_max'], 'pse_r': [int(r) for r in data]
    }}

    pprint(result)
    return result


def schwartz_zippel_runner(n, r):
    total = 0
    poly = polynomials[n - 2]

    # This was value intialized in the main function.
    # Let AxProf choose "r" value vector.
    d = [1] * len(poly)
    for index, item in enumerate(poly):
        total += item * (r[index] ** d[index])

    return 1 if total == 0 else 0


if __name__ == '__main__':
    # ForAll Polynomials settings.
    for degree in configList['n']:
        poly = []
        for i in range(degree):
            poly.append(random.randint(1, 15000))
        polynomials.append(poly)

    startTime = time.time()  # Start measuring time

    """
    We specify that we need to run each coin-flipping session, 1000 times.
    The number of coins flipped in each session is equal to the numbers
    listed in the configList defined above. 

    configList contains the ForAlls.
    """
    AxProf.checkProperties(configList, runs_per_input, num_input_samples, AxProf.distinctIntegerGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')

# ==============================================================================
