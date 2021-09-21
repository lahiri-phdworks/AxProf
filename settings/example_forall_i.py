import sys
import os
import random
import AxProf
import random
import math
import time
from scipy.stats import bernoulli
from IPython.lib.pretty import pprint

configList = {'k': [5],
              'a': [1000]
              }

spec = '''
Input list of real;
Output real;
TIME k;
ACC forall i in Input : Probability over runs [ Output > 2.5 * i && Output <= 5 * i ] > 0.95
'''

runs_per_input = 100  # 200
num_input_samples = 50  # 1


def inputParams(config, inputNum):
    return [1, 1, config['a']]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    print(data)
    output = getSum(int(data[0]))
    endTime = time.time()
    result = {'acc': output, 'time': (endTime - startTime), 'space': 0, 'summary': {
        'sum': output, 'a': int(data[0])
    }}

    pprint(result)
    return result


def getSum(a):
    """[summary]

    Args:
        a (int): [Program Input]

    Returns:
        r_sum [Output : int]: [Sum of 5 randomly sampled elements]
    """
    r = random.randint(0, a)  # 1st Sampling
    r_sum = 0

    for i in range(5):
        r_sum += random.randint(0, r)  # 2nd Sampling

    return r_sum


if __name__ == '__main__':
    startTime = time.time()  # Start measuring time

    AxProf.checkProperties(configList, runs_per_input, num_input_samples, AxProf.dummyGenerator,
                           inputParams, runner, spec=spec)

    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')
