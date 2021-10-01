import os
import sys
import time
import random
import AxProf
import subprocess
from scipy.stats import bernoulli
from IPython.lib.pretty import pprint

# n : Array Size ForAll Variable.
configList = {'n': [100, 150, 200]}
written_once = 0

# Axprof Specification for QuickSort Partitioning Algorithm.
# Pr() bound : Probability over runs [ Output == n/2 ] > 0.99 [Error]
spec = '''
Input real;
Output real;
n real;
TIME n;
ACC Expectation over runs [ Output ] > n/2 
'''

runs_per_input = 100
num_input_samples = 1


def inputParams(config, inputNum):
    return [config['n'], -10000, 10000]


def runner(inputFileName, config):
    startTime = time.time()
    global written_once
    data = []
    for line in open(inputFileName, "r"):
        data.append(int(line.strip()))

    if written_once == 0:
        with open(inputFileName, "w") as fileptr:
            written_once = 1
            fileptr.write(f"{config['n']}\n")
            for lines in data:
                fileptr.write(f"{lines}\n")

    # COMMENT : Do we add an assume(distinct) assert here for AxProf?
    time.sleep(0.25)
    pipes = subprocess.run(f"./bin/partition < {inputFileName}", shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    out, err = pipes.stdout, pipes.stderr
    out = out.decode("utf-8").strip()
    err = err.decode("utf-8").strip()
    endTime = time.time()
    print(f"{err}")
    result = {'acc': int(out), 'time': (endTime - startTime), 'space': 0}
    pprint(result)
    return result


if __name__ == '__main__':
    startTime = time.time()  # Start measuring time

    """
    We specify that we need to run each coin-flipping session, 1000 times.
    The number of coins flipped in each session is equal to the numbers
    listed in the configList defined above.

    configList contains the ForAlls.
    """
    AxProf.checkProperties(configList, runs_per_input, num_input_samples, AxProf.arrayGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')

# ==============================================================================
