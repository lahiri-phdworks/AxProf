import AxProf
import subprocess
import random
import sys

configlist = {'ressize': [i for i in range(50, 550, 10)],
              'datasize': [i for i in range(50, 550, 10)]}


def igparams(Cfg, inpNum): return [Cfg['datasize'], 1, 0]


ofname = 'resoutput.txt'
pfname = 'perfstats.txt'

spec = '''
Input list of real;
Output list of real;
min real;
TIME datasize;
SPACE ressize;
ACC forall i in Input : Probability over runs [ i in Output ] == min((ressize - 1)/datasize, 1)
'''


def runner(ifname, config):
    pipes = subprocess.run(args=['./bin/sample', '-k', str(config['ressize']),
                           '-d', str(random.randint(0, 2**31-1)), ifname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = pipes.stdout, pipes.stderr
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    err = err.split()
    err = [random.random(), random.random()]
    sample = set()
    out = out.split('\n')[:-1]
    for line in out:
        sample.add(int(line))
    return {'time': float(err[0]), 'space': float(err[1]), 'acc': sample}


if __name__ == "__main__":
    random.seed()
    subprocess.run(['date'])
    AxProf.checkProperties(configlist, 300, 1,
                           AxProf.linearGenerator, igparams, runner, spec=spec)
    subprocess.run(['date'])
