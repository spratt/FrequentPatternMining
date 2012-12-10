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

from collections import deque
import logging as log
from dataset import Dataset, NumericalDataset

######################################################################
# Configuration
######################################################################

name = 'fp_mining'
log_format = '[%(asctime)s %(funcName)s]: %(message)s'

######################################################################
# Logging Setup
######################################################################
log.basicConfig(filename=name+'_log.txt',\
                    level=log.INFO,\
                    format=log_format)

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
    keys = filter(lambda x: counts[x] >= min_sup,keys)
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
    keys = filter(lambda x: counts[x] >= min_sup,keys)
    candidates = map(lambda x: [x], keys)
    log.info('generated {0} k=1 candidates'.format(len(candidates)))
    for i in range(1,k):
        candidates = aprioriCandidatePatterns(ds,min_sup,candidates)
    log.info('found {0} k={1} patterns'.format(len(candidates),k))
    return candidates

######################################################################
# FP-Growth
######################################################################
# First we build a structure of information about frequent items
# called the FP-Tree, then we use this structure to find frequent
# patterns using the FP-Growth algorithm.
######################################################################

class FPTreeNode(object):
    def __init__(self,item,count,parent=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = []

    def addChild(self,node):
        self.children.append(node)

    def incCount(self,count=1):
        self.count += count

    def prefixPath(self):
        path = deque()
        node = self.parent
        while node.item != None:
            path.appendleft(node.item)
            node = node.parent
        return list(path)

    def gvNodeLabel(self):
        return '{0} [label="({1}:{2})"];\n'.\
            format(self.gvNodeName(),self.item,self.count)

    def gvNodeName(self):
        return 'fp_node_{0}'.format(str(id(self)))
    
class FPTree(object):
    def __init__(self):
        self.root = FPTreeNode(None,0)
        self.itemCounts = dict()
        self.itemNodes = dict()

    def __len__(self):
        return self.root.count

    def __str__(self):
        return self.gvString()

    def gvString(self):
        s = "digraph{\n"
        d = deque([self.root])
        while len(d) > 0:
            node = d.popleft()
            d.extend(node.children)
            s += node.gvNodeLabel()
            for child in node.children:
                s += '{0} -> {1};\n'.\
                    format(node.gvNodeName(),child.gvNodeName())
        return s + "}\n"

    def isSinglePath(self):
        node=self.root
        while len(node.children) > 0:
            if len(node.children) > 1:
                return False
            node = node.children[0]
        return True

    def addItemset(self,node,itemset):
        for item in itemset:
            # loop invariant: node is the child's parent
            child = FPTreeNode(item,1,node)
            self.registerNode(item,child)
            self.incItemCount(item)
            node.addChild(child)
            node = child

    def incItemCount(self,item,count=1):
        itemCounts = self.itemCounts
        if item in itemCounts:
            itemCounts[item] += count
        else:
            itemCounts[item] = count       

    def registerNode(self,item,node):
        itemNodes = self.itemNodes
        if item in itemNodes:
            itemNodes[item].append(node)
        else:
            itemNodes[item] = [node]

    def getConditionalPatternBase(self,item):
        base = []
        itemNodes = self.itemNodes
        if item not in itemNodes:
            return base
        for node in itemNodes[item]:
            prefixPath = node.prefixPath()
            if len(prefixPath) == 0:
                continue
            for _ in range(node.count):
                base.append(prefixPath)
        return base

    def updateItemset(self,itemset):
        """ takes a list of items, adds or updates a path in tree """

        node = self.root
        node.incCount()
        for (i,item) in enumerate(itemset):
            # loop invariant: node is a valid FPTreeNode
            children = node.children
            last = node
            node = None
            for child in children:
                if child.item == item:
                    node = child
                    break
            if node == None:
                self.addItemset(last,itemset[i:])
                return
            else:
                node.incCount()
                self.incItemCount(item)

def sortByFreq(l,counts,reverse=True):
    return sorted(l,key=lambda x: counts[x],reverse=reverse)
    
def buildFPTree(ds,min_sup):
    log.info('called on ds with {0} elements'.format(len(ds)))

    log.info('counting elements')
    counts = dict()
    for row in ds:
        rowCounts = countItems(row)
        counts = mergeCounts(counts,rowCounts)
    log.info('counted {0} elements'.format(len(counts)))

    log.info('finding the frequent elements')
    freqElmnts = set(filter(lambda x: counts[x] >= min_sup,counts.keys()))
    log.info('found {0} frequent elements'.format(len(freqElmnts)))

    log.info('building FP-Tree')
    fptree = FPTree()
    for row in ds:
        rowSet = set(row)
        freqItems = sortByFreq(list(rowSet & freqElmnts),counts)
        fptree.updateItemset(freqItems)
    log.info('built FP-Tree with {0} support'.format(fptree.root.count))
    log.info('root node has {0} children'.format(len(fptree.root.children)))
    log.info('FP-Tree is a single path? {0}'.format(fptree.isSinglePath()))
    return fptree

def combsOfSize(l,k):
    if k == 1:
        return map(lambda x: [x],l)
    combs = []
    if len(l) < k or k < 1:
        return combs
    for (i,x) in enumerate(l):
        for y in combsOfSize(l[i+1:],k-1):
            combs.append([x] + y)
    return combs

def allCombinations(l):
    combs = []
    for (i,x) in enumerate(l):
        combs.append([x])
        for y in allCombinations(l[i+1:]):
            combs.append([x] + y)
    return combs

def mineFPTree(fptree,k,min_sup):
    log.info('called')
    patterns = []

    # base case: fptree has a single path
    if fptree.isSinglePath():
        log.info('fptree has one path')
        counts = fptree.itemCounts
        candidatePatterns = filter(lambda x: counts[x] > min_sup,\
                                       counts.keys())
        log.info('{0} items have at least min_sup'.\
                     format(len(candidatePatterns)))
        candidatePatterns = combsOfSize(candidatePatterns,k)
        log.info('generated {0} candidate patterns'.\
                     format(len(candidatePatterns)))
        for cand in candidatePatterns:
            if len(cand) < k:
                continue
            patterns.append(cand)
        log.info('filtered candidates down to {0} patterns'.\
                     format(len(patterns)))
        return patterns

    log.info('fptree has many paths')
    log.info('building item list sorted by frequency ascending')
    counts = fptree.itemCounts
    items = counts.keys()
    items = sortByFreq(items,counts,False)
    log.info('found {0} items'.format(len(items)))
    log.info('first item: {0}, frequency: {1}'.\
                 format(items[0],counts[items[0]]))

    for item in items:
        cpb = fptree.getConditionalPatternBase(item)
        log.info('conditional pattern base for {0} has {1} rows'.\
                     format(item,len(cpb)))
    
        cfpt = buildFPTree(cpb,min_sup)
        log.info('generated conditional FP-Tree with {0} support'.\
                     format(len(cfpt)))

        cfp = mineFPTree(cfpt,k-1,min_sup)
        log.info('mined FP-Tree')
        for fp in cfp:
            pattern = fp + [item]
            if pattern not in patterns:
                patterns.append(pattern)
        log.info('generated {0} new patterns ending in {1}'.\
                     format(len(cfp),item))
    
    return patterns

def fpGrowthPatterns(ds,k,min_sup=0):
    log.info('called on ds with {0} elements'.format(len(ds)))
    
    log.info('building FP-Tree')
    fptree = buildFPTree(ds,min_sup)
    log.info('FP-Tree built')

    log.info('running FP-Growth on FP-Tree')
    patterns = mineFPTree(fptree,k,min_sup)
    log.info('FP-Growth found {0} patterns'.format(len(patterns)))

    return patterns

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

    if len(sys.argv) < 3:
        print "usage: {0} [file] [k] [results]".format(sys.argv[0])
        sys.exit(-1)

    filename = sys.argv[1]
    k = int(sys.argv[2])

    max_results = -1
    if len(sys.argv) > 3:
        max_results = int(sys.argv[3])
    
    ds = NumericalDataset()
    with open(filename,'rU') as f:
        ds.readFromFile(f)

    log.info('==================== fp_mining tests ====================')
    log.info("Read {0} lines in {1}".format(len(ds),filename))

    # run test here
    #patterns = print aprioriPatterns(ds,k,len(ds)/2)
    patterns = fpGrowthPatterns(ds,k,len(ds)/2)
    print 'found {0} patterns of size {1}'.format(len(patterns),k)
    if max_results == -1:
        max_results = len(patterns)
    for i in range(max_results):
        print patterns[i]
