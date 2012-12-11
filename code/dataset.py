#!/usr/bin/env python2.6
######################################################################
# dataset.py
######################################################################
# In which we define a Dataset object which stores rows of itemsets
# and can parse information from a file which separates itemsets by
# newlines and separates items within an itemset by a single space.
######################################################################
# For license information, see LICENSE file
# For copyright information, see COPYRIGHT file
######################################################################

from collections import defaultdict

######################################################################
# Dataset
######################################################################
# The most basic dataset which stores itemsets as rows.
######################################################################

class Dataset(object):
    def __init__(self):
        self.rows = []

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return iter(self.rows)

    def readFromFile(self,f):
        for line in f:
            canonical = line.strip().lower()
            self.rows.append(canonical.split(" "))

    def readFromDataset(self,ds):
        if not hasattr(ds,'__IS_VERTICAL__'):
            self.rows = []
            for row in ds.rows:
                self.rows.append(row[:])
            return
        
        transactions = defaultdict(list)
        for key in ds.tidsets.keys():
            for val in ds.tidsets[key]:
                transactions[val].append(key)
        self.rows = transactions.values()

######################################################################
# NumericalDataset
######################################################################
# This dataset also stores itemsets as rows, but converts the items to
# integers.
######################################################################

class NumericalDataset(Dataset):
    def _convertToNumerical(self):
        for row in range(len(self.rows)):
            for col in range(len(self.rows[row])):
                val = self.rows[row][col]
                self.rows[row][col] = int(val)
    
    def readFromFile(self,f):
        Dataset.readFromFile(self,f)
        self._convertToNumerical()

    def readFromDataset(self,ds):
        Dataset.readFromDataset(self,ds)
        self._convertToNumerical()

######################################################################
# VerticalDataset
######################################################################
# This dataset stores item values in a list of values and for each
# item value there is a list of itemsets in which it appears, these
# lists are stored in rows.
######################################################################

class VerticalDataset(Dataset):
    def __init__(self):
        self.tidsets = defaultdict(set)
        self.__IS_VERTICAL__ = True

    def _convertToVertical(self):
        transactions = self.rows

        tidsets = defaultdict(set)
        for (i,row) in enumerate(transactions):
            for val in row:
                tidsets[val].add(i)

        self.tidsets = tidsets

    def readFromFile(self,f):
        Dataset.readFromFile(self,f)
        self._convertToVertical()
    
    def readFromDataset(self,ds):
        if hasattr(ds,'__IS_VERTICAL__'):
            self.rows = ds.rows[:]
            self.values = ds.values[:]
            return
        Dataset.readFromDataset(self,ds)
        self._convertToVertical()
                
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
    for row in ds.rows:
        print row

    vds = VerticalDataset()
    vds.readFromDataset(ds)
    for key in vds.tidsets.keys():
        print "{0}:{1}".format(key,vds.tidsets[key])

    ds.readFromDataset(vds)
    for row in ds.rows:
        print row
