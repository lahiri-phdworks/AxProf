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
configList = {'entries': [3, 4, 5, 6, 7]}

# Axprof Specification for Bloom Filter
spec = '''
Input list of real;
Output list of real;
p real;
ACC Probability over i in excluded(Config, Input) [ i in Output ] < p
'''


runs_per_input = 10
num_input_samples = 20
forall_strings = []


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
    return [2, 0, config['entries'] - 1]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    # data[0] is the false positive rate
    output = 0

    output = bloom_filter_runner(
        config['entries'], config['error'], int(data[0]), int(data[1]), config['forall_settings'])

    endTime = time.time()
    result = {'acc': output, 'time': (endTime - startTime), 'space': 0, 'random input': {
        'error': config['error'], 'entries': config['entries'], 'add_index': int(data[0]), 'seach_index': int(data[1]), 'forall_setting': config['forall_settings']
    }}
    pprint(result)
    return result


def bloom_filter_runner(entries, error, add_key, search_key, forall_input):
    with open(f"tests/bloomfilter_{entries}.txt", mode="w") as fileptr:
        fileptr.write(f"{entries}\n")
        fileptr.write(f"{entries}\n")
        fileptr.write(f"{error}\n")
        fileptr.write(f"{add_key}\n")
        fileptr.write(f"{search_key}\n")
        for strings in forall_strings[forall_input][entries - 3]:
            fileptr.write(f"{strings}\n")
    return execute(f"tests/bloomfilter_{entries}.txt", f"tests/output_{entries}.txt", f"tests/error_{entries}.txt")


if __name__ == '__main__':
    # Generate a set of strings that are to be added to the bloomfilter.
    errors = []
    for i in range(25):
        errors.append(random.uniform(0.01, 0.999))

    configList['error'] = errors
    configList['forall_settings'] = range(10)

    for k in configList['forall_settings']:
        string_data_set = []
        for entries in configList['entries']:
            string_data = []
            for j in range(entries):
                strings = ''.join(random.SystemRandom().choice(
                    string.ascii_uppercase + string.digits) for _ in range(10))
                string_data.append(strings)
            string_data_set.append(string_data)
        forall_strings.append(string_data_set)

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
