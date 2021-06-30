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
configList = {'choice': [1, 2, 3],
              'door_switch': [0, 1]}

# Axprof Specification for Monty Hall
spec = '''
Input real;
Output real;
choice real;
door_switch real;
ACC Probability over inputs [ Output == 1 ] >= 2/3
'''

runs_per_input = 1
num_input_samples = 500


def inputParams(config, inputNum):
    return [1, 1, 3]


def runner(inputFileName, config):
    startTime = time.time()

    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    output = monty_hall_runner(
        # choice,         door_switch,           car_door
        config['choice'], config['door_switch'], int(data[0]))

    if output is False:
        output = 0
    else:
        output = 1

    endTime = time.time()
    result = {'acc': output, 'time': (
        endTime - startTime), 'space': 0, 'random input': {'forall_choice': config['choice'],
                                                           'forall_door_switch': config['door_switch'], 'pse_car_door': int(data[0])}}
    pprint(result)
    return result


def monty_hall_runner(choice, door_switch, car_door):
    if choice == car_door:
        return door_switch != 1
    else:
        host_door = 0
        if choice != 1 and car_door != 1:
            host_door = 1
        elif choice != 2 and car_door != 2:
            host_door = 2
        else:
            host_door = 3

        if door_switch == 1:
            if host_door == 1:
                if choice == 2:
                    choice = 3
                else:
                    choice = 2
            elif host_door == 2:
                if choice == 1:
                    choice = 3
                else:
                    choice = 1
            else:
                if choice == 1:
                    choice = 2
                else:
                    choice = 1
        return choice == car_door


if __name__ == '__main__':
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
