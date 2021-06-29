# AxProf Tutorial : checking if a coin is fair
# Tweaking the tutorial parameters

import AxProf
import random
import sys
import time
from scipy.stats import bernoulli

# We want to try with these number of coins the flipping experiment.
# We specify number of coin-flips here .


# coins : n -> this is a ForAll Variable.
# prob : p -> ForAll Variable
# y : addendum if flip is 1, ForAll Variable
configList = {'coins': [500, 1500, 2500, 5000],
              'prob': [0.01, 0.09, 0.10, 0.20, 0.25, 0.375, 0.50, 0.67, 0.75, 0.85, 0.90],
              'y': [5, 10, 20, 30, 50, 85, 96, 100]}

# ==============================================================================

# The specification consists of a list of type
# declarations, followed by a TIME specification, SPACE specification, and
# ACCuracy specification. The specifications are optional, but they must be
# present in this order. Each type declaration or specification must be
# separated by a semicolon. The type of the Input and the Output must always
# be declared. The return type of any external functions used must also be
# declared.

spec = '''
Input list of real;
Output real;
prob real;
y real;
TIME coins;
ACC Expectation over runs [Output] == coins * prob * y
'''


random_runs = 1000
random_input_samples = 1


# y -> ForAll Variable
# ACC Expectation over runs [Output] == coins * prob * y
# The generator takes 3 parameters: the number of integers to generate, the minimum
# integer value, and the maximum integer value. The full list of generators is
# available in AxProf/AxProfGenerators.py in the artifact.


def inputParams(config, inputNum):
    return [config['coins'], 0, 1000000]

# This tells AxProf's distinctIntegerGenerator to generate distinct integers
# between 0 and 1000000. The number of integers generated is equal to the number
# of coins.


def runner(inputFileName, config):

    startTime = time.time()  # Start measuring time

    """
    We read the data that is generated by the input
    generator that AxProf uses. This example however does
    not need it. 

    In-case of other examples, we can read and use this generated 
    data to our use in the function that the runner() calls. 
    """
    data = []
    for line in open(inputFileName, "r"):
        data.append(line[:-1])

    """[Let's Flip Coins]

    The runner is run "n" times where "n" is len(configList). 
    Each time with the next value in the configList.
    Returns:
        [Sum]: [NUmber of HEADS in the coin flip experiment]
    """
    coinSum = flipCoins(
        config['coins'], config['prob'], config['y'])  # flipCoins(config['coins']) Same Value as expected.

    endTime = time.time()  # Stop measuring time

    # Prepare result; we don't measure memory but must specify it, so set it to 0
    result = {'acc': coinSum, 'time': (endTime - startTime), 'space': 0}
    return result

    """[What flipCoin does?]
        The flipCoins function flips the coins, adds their face values, measures the
        time taken to do so, and returns the output. In this simple case, this
        function comprises the entirety of the implementation of the coin flip program
        that we are testing with AxProf. The rest of the code is used to test this
        implementation using AxProf.
    """


"""
This function returns the result of the experiment we conduct by 
flipping number of coins == numCoins with H/T based on a dist. 
"""


def flipCoins(n, prob, y):
    random.seed()  # Seed RNG
    coinSum = 0
    for i in range(n):

        # Set x = 0. Instead of random-choice
        # it is a bernoulli.rvs(p, size=1)
        r = bernoulli.rvs(prob, size=1)
        if (r):
            coinSum += y

        # TODO : Modify this. Set x = 0, and for each random-choice x = x + y
    return coinSum

# ==============================================================================

# Finally, we invoke AxProf's checkProperties function. It takes the following
# parameters:
# 1) The list of configurations to test.
# 2) The number of times the implementation should be run. Setting this to None
#    will allow AxProf to choose the number of runs automatically based on the
#    statistical test used.
# 3) The number of different inputs to test the implementation with.
# 4) The type of input generator to use.
# 5) The function used to give parameters to the input generator.
# 6) The runner i.e. the application interface.
# Apart from this, it takes multiple optional parameters. Usually, only the
# specification` needs to be provided. AxProf will generate all necessary code
# from the specification and use it to test the program.
# It is important to use `if __name__ == '__main__':` when invoking AxProf. We
# also measure the total time taken to use AxProf.


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
