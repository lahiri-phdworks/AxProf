# Local Sensitive Hashing Algorithm.

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
              'l': [5],
              'a': [1000000000]
              }

spec = '''
Input list of real;
Output list of real;
TIME k;
ACC forall i in indices(Input), q in indices(Input) : 
        Probability over runs [ [q, i] in Output ] == L1HashEqProb(Input[i], Input[q], 10, k, l)
'''

runs_per_input = 5  # 200
num_input_samples = 2  # 1


def inputParams(config, inputNum):
    return 1, 1, config['a']


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    print(data)
    output = retOut(1, 1, 10, 5, 5)
    endTime = time.time()
    result = {'acc': output, 'time': (endTime - startTime), 'space': 0, 'summary': {
        'output': output, 'a': int(data[0])
    }}

    pprint(result)
    return result


def retOut(inp_i, inp_q, conf=10, num_hash_funcs=5, num_hash_tables=5):
    return [inp_i, inp_q]


def L1HashEqProb(inp_i, inp_q, conf=10, num_hash_funcs=5, num_hash_tables=5):
    return 0.15


if __name__ == '__main__':
    startTime = time.time()  # Start measuring time

    AxProf.checkProperties(configList, runs_per_input, num_input_samples, AxProf.distinctIntegerGenerator,
                           inputParams, runner, spec=spec)

    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')
