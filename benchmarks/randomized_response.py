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
truth real;
first_flip real;
second_flip real;
ACC Expectation over runs [Output] == ???
'''


def inputParams(config, inputNum):
    return [config['second_flip'], 0, 1]


def runner():
    pass


def randomized_response_runner():
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
