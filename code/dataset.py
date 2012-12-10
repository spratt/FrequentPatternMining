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

class NumericalDataset(Dataset):
    def readFromFile(self,f):
        Dataset.readFromFile(self,f)
        for row in range(len(self.rows)):
            for col in range(len(self.rows[row])):
                val = self.rows[row][col]
                self.rows[row][col] = int(val)

class VerticalDataset(Dataset):
    def __init__(self):
        self.rows = []
        self.__IS_VERTICAL__ = True
    
    def readFromDataset(self,ds):
        transactions = ds.rows[:]
        if hasattr(ds,'__IS_VERTICAL__'):
            self.rows = transactions
            self.values = ds.values[:]
            return

        values = []
        for row in transactions:
            for val in row:
                if val not in values:
                    values.append(val)

        rows = [[] for _ in values]
        for (i,row) in enumerate(transactions):
            for val in row:
                rows[values.index(val)].append(i)

        self.values = values
        self.rows = rows
            
                
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
    for (i,val) in enumerate(vds.values):
        print "{0}:{1}".format(i,val)
    for row in vds.rows:
        print row
