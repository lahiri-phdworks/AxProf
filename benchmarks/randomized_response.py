import sys
import os
import random
import AxProf
import random
import time
from scipy.stats import bernoulli


# choice : ForAll Variable.
# door_switch : ForAll Variable
configList = {'truth': [0, 1],
              'first_flip': [0, 1], 'second_flip': [1]}

# Axprof Specification for Monty Hall
spec = '''
Input list of real;
Output real;
truth real;
first_flip real;
second_flip real;
ACC Probability over runs [ Output == truth ] > 0.5
'''

random_runs = 1
random_input_samples = 1


def inputParams(config, inputNum):
    # Randomly choose the second flip from AxProf.
    return [config['second_flip'], 0, 1]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    output = randomized_response_runner(data[0], data[1], data[2])

    endTime = time.time()
    result = {'acc': output, 'time': (
        endTime - startTime), 'space': 0, 'random input': data}

    print(result)
    return result


def randomized_response_runner(truth, first_flip, second_flip):
    if first_flip == 0:
        ret = truth
    else:
        if second_flip == 1:
            ret = 1
        else:
            ret = 0
    pass


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
