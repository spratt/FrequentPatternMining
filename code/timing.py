#!/usr/bin/env python2.6
######################################################################
# timing.py
######################################################################
# A script for comparative timings of FP algorithms.
######################################################################
# For license information, see LICENSE file
# For copyright information, see COPYRIGHT file
######################################################################

import sys
from timeit import Timer
from dataset import Dataset, NumericalDataset, VerticalDataset
from fp_mining import aprioriPatterns, fpGrowthPatterns, eclatPatterns

######################################################################
# Configuration
######################################################################

filepath = '../data/'

tiny_files = ['tiny.dat']
files = ['chess_tiny.dat','chess_small.dat','chess.dat']

tiny_sizes = [1,2]
sizes = [1,2,3,4,5]

tiny_runs = 1000
runs = 1

trials = 1

if len(sys.argv) > 1:
    runs = int(sys.argv[1])
    runs = runs if runs > 0 else 1

if len(sys.argv) > 2:
    trials = int(sys.argv[2])
    trials = trials if trials > 0 else 1

support_percents = [.1,.2,.3,.4,.5]

######################################################################
# Logic
######################################################################

class Incrementor(object):
    def __init__(self,value=0):
        self.i = value

    def retInc(self):
        old = self.i
        self.i += 1
        return old

i = Incrementor()

def timePatterns(ds,k,min_sup,runs):
    timers = {}
    timers['apriori'] = Timer(lambda: aprioriPatterns(ds,k,min_sup))
    timers['fp-growth'] = Timer(lambda: fpGrowthPatterns(ds,k,min_sup))
    timers['eclat'] = Timer(lambda: eclatPatterns(ds,k,min_sup))

    for key in timers.keys():
        timer = timers[key]
        print "{0},{1},{2},{3},{4},{5},{6}".format(\
            i.retInc(),key,len(ds),k,min_sup,runs,timer.timeit(runs))

for _ in range(trials):
    # run tiny tests
    for tiny_file in tiny_files:
        ds = Dataset()
        with open(filepath + tiny_file,'rU') as f:
            ds.readFromFile(f)

        for size in tiny_sizes:
            for prct in support_percents:
                min_sup = int(prct * float(len(ds)))
                timePatterns(ds,size,min_sup,tiny_runs)

    # run tests
    if runs < 1:
        continue

    for filename in files:
        ds = Dataset()
        with open(filepath + filename,'rU') as f:
            ds.readFromFile(f)

        for size in sizes:
            for prct in support_percents:
                min_sup = int(prct * float(len(ds)))
                timePatterns(ds,size,min_sup,runs)
