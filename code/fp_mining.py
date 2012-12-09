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

from dataset import Dataset, NumericalDataset
import logging as log

######################################################################
# Configuration
######################################################################

name = 'fp_mining'
format = '[%(asctime)s %(funcName)s]: %(message)s'.format(name)
log.basicConfig(filename=name+'_log.txt',level=log.INFO,format=format)

######################################################################
# Apriori
######################################################################
# This algorithm is based on the antimonotone property of frequent
# itemsets.  That is to say, subsets of frequent itemsets must
# themselves be frequent itemsets.  With this in mind, to find
# frequent itemsets of size k, we begin by finding all frequent
# itemsets of size 1, then of size 2, ..., then of size k-1, then
# finally we can find the frequent itemsets of size k.
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
    itemset = set(row)
    for cand in cands:
        candSet = set(cand)
        counts[str(cand)] = 1 if candSet <= itemset else 0
    return counts

def mergeCounts(counts1,counts2):
    """ Takes two count dicts and returns the dict merge of both """
    merge = dict()
    for key in counts1.keys() + counts2.keys():
        merge[key] = 0
        if key in counts1:
            merge[key] += counts1[key]
        if key in counts2:
            merge[key] += counts2[key]
    return merge

def sort(l):
    m = l[:]
    m.sort()
    return m

def aprioriCandidatePatterns(ds,min_sup,prevCands=None):
    """ given dataset ds, min_sup, and prevCands, find next candidates """
    log.info('called')
    if len(prevCands) == 0:
        return []
    if prevCands == None:
        prevCands = [[]]
    k = len(prevCands[0]) + 1
    items = map(lambda x: [x],set(reduce(lambda x,y: x+y, prevCands)))
    cands = []
    for prevCand in prevCands:
        for item in items:
            if item[0] not in prevCand:
                cands.append(prevCand + item)
    log.info('generated {0} k={1} candidates'.format(len(cands),k))
    cands = list(set(map(lambda x: str(sort(x)),cands)))
    cands = map(lambda x: eval(x),cands)
    log.info('generated {0} k={1} canonical candidates'.format(len(cands),k))
    counts = dict()
    for row in ds:
        rowCounts = countCandidates(row,cands)
        counts = mergeCounts(counts,rowCounts)
    log.info('counted candidate pattern occurrences')
    keys = counts.keys()
    keys = filter(lambda x: counts[x] > min_sup,keys)
    candidates = map(lambda x: eval(x),keys)
    log.info('found {0} k={1} patterns'.format(len(candidates),k))
    return candidates

def aprioriPatterns(ds,k,min_sup=0):
    """ given dataset ds, find frequent k-patterns with min support min_sup """
    log.info('called')
    counts = dict()
    for row in ds:
        rowCounts = countItems(row)
        counts = mergeCounts(counts,rowCounts)
    keys = counts.keys()
    keys = filter(lambda x: counts[x] > min_sup,keys)
    candidates = map(lambda x: [x], keys)
    log.info('generated {0} k=1 candidates'.format(len(candidates)))
    for i in range(1,k):
        candidates = aprioriCandidatePatterns(ds,min_sup,candidates)
    log.info('found {0} k={1} patterns'.format(len(candidates),k))
    return candidates

def testApriori(ds):
    print aprioriPatterns(ds,5,len(ds)/2)

######################################################################
# FP-Growth
######################################################################
# First we build a structure of information about frequent items
# called the FP-Tree, then we use this structure to find frequent
# patterns using the FP-Growth algorithm.
######################################################################

def buildFPTree(ds):
    log.info('called on ds with {0} elements'.format(len(ds)))

    log.info('counting elements')
    counts = dict()
    for row in ds:
        rowCounts = countItems(row)
        counts = mergeCounts(counts,rowCounts)
    log.info('counted {0} elements'.format(len(counts)))

    log.info('transforming dictionary into sorted tuples')
    countTuples = []
    for key in counts.keys():
        countTuples.append((key,counts[key]))
    countTuples = sorted(countTuples, key = lambda x: x[1], reverse=True)
    for t in countTuples:
        log.info('Found tuple {0}'.format(t))
    log.info('transformed')
        
    return countTuples

def mineFPTree(fptree,k,min_sup):
    log.info('called')
    return []

def fpGrowthPatterns(ds,k,min_sup=0):
    log.info('called on ds with {0} elements'.format(len(ds)))
    
    log.info('building FP-Tree')
    fptree = buildFPTree(ds)
    log.info('FP-Tree built')

    log.info('running FP-Growth on FP-Tree')
    patterns = mineFPTree(ds,k,min_sup)
    log.info('FP-Growth found {0} patterns'.format(len(patterns)))

    return patterns

def testFPGrowth(ds):
    print fpGrowthPatterns(ds,5,len(ds)/2)

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
    ds = NumericalDataset()
    with open(filename,'rU') as f:
        ds.readFromFile(f)
    print "Read {0} lines in {1}".format(len(ds),filename)

    # run test here
    #testApriori(ds)
    testFPGrowth(ds)
