import AxProf
import numpy as np
import subprocess
from collections import Counter
from numpy import log
import sys

sys.path.append('../AxProf')

configlist = {'logdelta': [-1, -2, -3],
              'epsilon': [0.05, 0.1, 0.2],
              'datasize': range(10000, 40000, 10000),
              'zipf': [1.1, 1.5, 2]}


def igparams(Cfg, inpNum): return [Cfg['datasize'], Cfg['zipf']]


commstr = """bin/countmin {} {} {} {}"""

spec = '''
Input list of real;
Output map from real to real;
count real;
TIME logdelta*datasize;
SPACE logdelta/(epsilon^2);
ACC Probability over i in uniques(Input) [ abs(count(i,Input) - Output[i]) > epsilon*|Input| ] < 1 - (10^logdelta)
'''


def count(i, Input):
    counts = Counter(Input)
    return counts[i]


def runner(ifname, config):
    query_str = commstr.format(config['datasize'], ifname,
                               config['epsilon'], 10**config['logdelta'])
    pipes = subprocess.run(query_str, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    out, err = pipes.stdout, pipes.stderr
    out = out.decode("utf-8").split('\n')
    err = err.decode("utf-8")
    output = {}
    time = float(out[1])
    output['time'] = time
    space = float(out[2])
    output['space'] = space
    output['acc'] = {}
    for line in out[3:-1]:
        _id, real, count = line.split(' ')
        output['acc'][int(_id)] = int(count)
    return output


# These functions are needed for input feature selection
def error(inputData, output):
    counts = Counter(inputData)
    errorSize = 0
    for item in output.keys():
        errorSize += output[item] - counts[item]
    return errorSize


if __name__ == "__main__":
    subprocess.run(['date'])
    AxProf.selectInputFeatures(configlist, AxProf.zipfGenerator,
                               igparams, ['datasize', 'zipf'], error,
                               runner)
    AxProf.checkProperties(configlist, None, 1, AxProf.zipfGenerator,
                           igparams, runner, spec=spec)
    subprocess.run(['date'])
    subprocess.run(['rm', '-f', 'gmon.out'])
