import sys
import os
import random
import AxProf
import random
import string
import time
from scipy.stats import bernoulli
from subprocess import run, CalledProcessError
from IPython.lib.pretty import pprint

# n : ForAll Variable. Entries in bloomfilter
configList = {'n': [3, 4, 5, 6, 7]}

# Axprof Specification for Bloom Filter
spec = '''
Input list of real;
Output real;
n real;
ACC Probability over inputs [ Output == 1 ] >= 0.5
'''


runs_per_input = 1
num_input_samples = 1
string_data_set = []


def execute(inFile, outfile, errFile):
    try:
        output = run(
            f"bin/bloomfilter < {inFile} > {outfile} 2> {errFile}",
            shell=True,
            capture_output=False,
            text=True,
        )
    except CalledProcessError as err:
        print(f"Execute Error : {err}")
    else:
        output = run(["cat", f"{outfile}"], capture_output=True)
        return int(output.stdout)


def inputParams(config, inputNum):
    return [0.01, 0.99]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    # data[0] is the false positive rate
    output = 0
    output = bloom_filter_runner(config['n'], float(data[0]))

    endTime = time.time()
    result = {'acc': output, 'time': (endTime - startTime), 'space': 0}
    pprint(result)
    return result


def bloom_filter_runner(entries, error):
    with open(f"tests/bloomfilter_{entries}.txt", mode="w") as fileptr:
        fileptr.write(f"{entries}\n")
        fileptr.write(f"{entries}\n")
        fileptr.write(f"{error}\n")
        fileptr.write(f"{random.randint(0, entries - 1)}\n")
        fileptr.write(f"{random.randint(0, entries - 1)}\n")
        for strings in string_data_set[entries - 3]:
            fileptr.write(f"{strings}\n")
    return execute(f"tests/bloomfilter_{entries}.txt", f"tests/output_{entries}.txt", f"tests/error_{entries}.txt")


if __name__ == '__main__':
    # Generate a set of strings that are to be added to the bloomfilter.
    for entries in configList['n']:
        string_data = []
        for j in range(entries):
            strings = ''.join(random.SystemRandom().choice(
                string.ascii_uppercase + string.digits) for _ in range(10))
            string_data.append(strings)
        string_data_set.append(string_data)

    startTime = time.time()  # Start measuring time

    """
    We specify that we need to run each coin-flipping session, 1000 times.
    The number of coins flipped in each session is equal to the numbers
    listed in the configList defined above. 

    configList contains the ForAlls.
    """
    AxProf.checkProperties(configList, runs_per_input, num_input_samples, AxProf.singleUniformGenerator,
                           inputParams, runner, spec=spec)
    endTime = time.time()  # Stop measuring time
    print(f'Total time required for checking : {endTime - startTime} seconds.')

# ==============================================================================
