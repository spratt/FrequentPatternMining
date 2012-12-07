#!/usr/bin/env python2.6
######################################################################
# frequent_pattern_dataset.py
######################################################################
# In which we implement frequent pattern mining algorithms on a
# dataset.
######################################################################
# For license information, see LICENSE file
# For copyright information, see COPYRIGHT file
######################################################################

from dataset import Dataset

class FrequentPatternDataset(Dataset):
    def aprioriPatterns(self,k):
        pass

    def fpGrowthPatterns(self,k):
        pass

    def eclatPatterns(self,k):
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
    ds = FrequentPatternDataset()
    with open(filename,'rU') as f:
        ds.readFromFile(f)
        
    print "Read {0} lines in {1}".format(len(ds),filename)
    print ds.aprioriPatterns(5)
    print ds.fpGrowthPatterns(5)
    print ds.eclatPatterns(5)
