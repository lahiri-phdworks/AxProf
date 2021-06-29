import sys
import os
import random
import AxProf
import random
import time
from scipy.stats import bernoulli
from subprocess import run, CalledProcessError

# choice : ForAll Variable.
# door_switch : ForAll Variable
configList = {'choice': [1, 2, 3],
              'door_switch': [0, 1], 'car_door': [1]}

# Axprof Specification for Monty Hall
spec = '''
Input list of real;
Output real;
prob real;
y real;
TIME coins;
ACC Expectation over runs [Output] == coins * prob * y
'''


random_runs = 1
random_input_samples = 1


def execute(executable, inFile, outfile, errFile):
    try:
        output = run(
            f"bin/{executable} < {inFile} > {outfile} 2> {errFile}",
            shell=True,
            capture_output=False,
            text=True,
        )
    except CalledProcessError as err:
        print(f"Execute Error : {err}")
    else:
        pass
    return output.returncode


def inputParams(config, inputNum):
    return [config['coins'], 1, 3]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    output = bloom_filter_runner(config['n'], data)

    endTime = time.time()
    result = {'acc': output, 'time': (endTime - startTime)}
    return result


def bloom_filter_runner():
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
