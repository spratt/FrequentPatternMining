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

######################################################################
# Apriori
######################################################################

def countItems(row):
    """ counts items in a row (list), returns a dict(item -> count) """
    counts = dict()
    for e in row:
        if e in counts.keys():
            counts[e] += 1
        else:
            counts[e] = 1
    return counts

def countCandidates(row,cands):
    counts = dict()
    for cand in cands:
        counts[str(cand)] = 0
    

def aprioriCandidatePatterns(ds,min_sup,prevCands):
    """ given dataset ds, min_sup, and prevCands, find next candidates """
    if len(prevCands) == 0:
        return []
    k = len(prevCands[0]) + 1
    items = map(lambda x: [x],set(reduce(lambda x,y: x+y, prevCands)))
    cands = []
    for prevCand in prevCands:
        for item in items:
            cands.append(prevCand + item)
            

def aprioriPatterns(ds,k,min_sup=0):
    """ given dataset ds, find frequent k-patterns with min support min_sup """
    counts = dict()
    for row in ds:
        rowCounts = countItems(row)
        for item in rowCounts.keys():
            if item in counts:
                counts[item] += rowCounts[item]
            else:
                counts[item] = rowCounts[item]
    keys = counts.keys()
    keys = filter(lambda x: counts[x] > min_sup,keys)
    candidates = map(lambda x: [x], keys)
    for i in range(1,k):
        candidates = aprioriCandidatePatterns(ds,min_sup,candidates)
    return candidates
        

######################################################################
# FP-Growth
######################################################################

def fpGrowthPatterns(ds,k):
    pass

######################################################################
# Eclat
######################################################################

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
    print aprioriPatterns(ds,1)
    print aprioriPatterns(ds,1,1000)
    print aprioriPatterns(ds,1,2000)
    print aprioriPatterns(ds,1,3000)
    print fpGrowthPatterns(ds,5)
    print eclatPatterns(ds,5)
