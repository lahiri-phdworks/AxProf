import sys
import os
import random
import AxProf
import random
import time
from scipy.stats import bernoulli
from IPython.lib.pretty import pprint

# choice : ForAll Variable.
# door_switch : ForAll Variable
configList = {'prime': [3, 5, 7, 11, 13, 17], 'forall_setting': range(100)}

# Axprof Specification for Monty Hall
spec = '''
Input list of real;
Output real;
ACC Probability over inputs [ Output == 1 ] >= 0.5
'''


runs_per_input = 1
num_input_samples = 10
forall_inputs = []

# 2 ==> since we need a_j, & b_j


def inputParams(config, inputNum):
    return [2, 0, config['prime']]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    w = random.randint(1, config['prime'])
    output = zp_hash_runner(config['forall_setting'], int(data[0]),
                            int(data[1]), config['prime'], w)

    endTime = time.time()
    result = {'acc': output, 'time': (endTime - startTime), 'space': 0, 'space': 0, 'random input': {
        'prime': config['prime'], 'a_j': int(data[0]), 'b_j': int(data[1]), 'w': w, 'forall_setting': config['forall_setting']
    }}
    pprint(result)
    return result


def zp_hash_runner(forall_index, a_j, b_j, prime, w):
    x = forall_inputs[forall_index][0]
    y = forall_inputs[forall_index][1]

    hash_x = (a_j * x + b_j) % prime % w
    hash_y = (a_j * y + b_j) % prime % w

    if (hash_x == hash_y):
        return 1
    else:
        return 0


if __name__ == '__main__':
    for index in configList['forall_setting']:
        forall_inputs.append(
            [random.randint(-5000, 5000), random.randint(5100, 10000)])

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
