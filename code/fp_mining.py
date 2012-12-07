#!/usr/bin/env python2.6
######################################################################
# fp_mining.py
######################################################################
# In which we implement frequent pattern mining algorithms on a
# dataset.
######################################################################
# For license information, see LICENSE file
# For copyright information, see COPYRIGHT file
######################################################################

from dataset import Dataset

def aprioriPatterns(ds,k):
    pass

def fpGrowthPatterns(ds,k):
    pass

def eclatPatterns(ds,k):
    pass

######################################################################
# Basic Tests
######################################################################
if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print "usage: {0} [file]".format(sys.argv[0])
        sys.exit(-1)

    filename = sys.argv[1]
    ds = Dataset()
    with open(filename,'rU') as f:
        ds.readFromFile(f)
        
    print "Read {0} lines in {1}".format(len(ds),filename)
    print aprioriPatterns(ds,5)
    print fpGrowthPatterns(ds,5)
    print eclatPatterns(ds,5)
