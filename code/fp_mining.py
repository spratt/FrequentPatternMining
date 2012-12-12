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
from itertools import combinations
import logging
import logging.config
from dataset import Dataset, NumericalDataset, VerticalDataset

######################################################################
# Logging Setup
######################################################################

logging.config.fileConfig('../config/logging.conf')
log = logging.getLogger('fpLog')

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
    log.debug('called')
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
    log.debug('generated {0} k={1} candidates'.format(len(cands),k))
    cands = list(set(map(lambda x: str(sort(x)),cands)))
    cands = map(lambda x: eval(x),cands)
    log.debug('generated {0} k={1} canonical candidates'.format(len(cands),k))
    counts = dict()
    for row in ds:
        rowCounts = countCandidates(row,cands)
        counts = mergeCounts(counts,rowCounts)
    log.debug('counted candidate pattern occurrences')
    keys = counts.keys()
    keys = filter(lambda x: counts[x] >= min_sup,keys)
    candidates = map(lambda x: eval(x),keys)
    log.debug('found {0} k={1} patterns'.format(len(candidates),k))
    return candidates

def aprioriPatterns(ds,k,min_sup=0):
    """ given dataset ds, find frequent k-patterns with min support min_sup """
    log.debug('called')
    counts = dict()
    for row in ds:
        rowCounts = countItems(row)
        counts = mergeCounts(counts,rowCounts)
    keys = counts.keys()
    keys = filter(lambda x: counts[x] >= min_sup,keys)
    candidates = map(lambda x: [x], keys)
    log.debug('generated {0} k=1 candidates'.format(len(candidates)))
    for i in range(1,k):
        candidates = aprioriCandidatePatterns(ds,min_sup,candidates)
    log.info('found {0} k={1} patterns'.format(len(candidates),k))
    return candidates

######################################################################
# FP-Growth
######################################################################
# First we build a structure of information about frequent items
# called the FP-Tree.  This tree stores nodes representing items in
# the dataset and the number of times the prefix formed by the path
# from the root to the node appears in itemsets in the dataset.
#
# Next, we mine the FP-Tree.  If the FP-Tree consists of a single
# path, then all combinations of items along the path are frequent
# patterns.  If the FP-Tree has many paths, we go through each item
# and build conditional FP-Trees containing that item, recursively
# mining those trees.
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
    log.debug('called on ds with {0} elements'.format(len(ds)))

    log.debug('counting elements')
    counts = dict()
    for row in ds:
        rowCounts = countItems(row)
        counts = mergeCounts(counts,rowCounts)
    log.debug('counted {0} elements'.format(len(counts)))

    log.debug('finding the frequent elements')
    freqElmnts = set(filter(lambda x: counts[x] >= min_sup,counts.keys()))
    log.debug('found {0} frequent elements'.format(len(freqElmnts)))

    log.debug('building FP-Tree')
    fptree = FPTree()
    for row in ds:
        rowSet = set(row)
        freqItems = sortByFreq(list(rowSet & freqElmnts),counts)
        fptree.updateItemset(freqItems)
    log.debug('built FP-Tree with {0} support'.format(fptree.root.count))
    log.debug('root node has {0} children'.format(len(fptree.root.children)))
    log.debug('FP-Tree is a single path? {0}'.format(fptree.isSinglePath()))
    return fptree

def combsOfSize(l,k):
    return [list(val) for val in combinations(l,k)]

def mineFPTree(fptree,k,min_sup):
    log.debug('called')
    patterns = []

    # base case: fptree has a single path
    if fptree.isSinglePath():
        log.debug('fptree has one path')
        counts = fptree.itemCounts
        candidatePatterns = filter(lambda x: counts[x] >= min_sup,\
                                       counts.keys())
        log.debug('{0} items have at least min_sup'.\
                     format(len(candidatePatterns)))
        candidatePatterns = combsOfSize(candidatePatterns,k)
        log.debug('generated {0} candidate patterns'.\
                     format(len(candidatePatterns)))
        for cand in candidatePatterns:
            if len(cand) < k:
                continue
            patterns.append(cand)
        log.debug('filtered candidates down to {0} patterns'.\
                     format(len(patterns)))
        return patterns

    log.debug('fptree has many paths')
    log.debug('building item list sorted by frequency ascending')
    counts = fptree.itemCounts
    items = counts.keys()
    items = sortByFreq(items,counts,False)
    log.debug('found {0} items'.format(len(items)))
    log.debug('first item: {0}, frequency: {1}'.\
                 format(items[0],counts[items[0]]))

    if k == 1:
        return map(lambda x: [x],items)
    
    for item in items:
        cpb = fptree.getConditionalPatternBase(item)
        log.debug('conditional pattern base for {0} has {1} rows'.\
                     format(item,len(cpb)))
    
        cfpt = buildFPTree(cpb,min_sup)
        log.debug('generated conditional FP-Tree with {0} support'.\
                     format(len(cfpt)))

        cfp = mineFPTree(cfpt,k-1,min_sup)
        log.debug('mined FP-Tree')
        for fp in cfp:
            pattern = fp + [item]
            if pattern not in patterns:
                patterns.append(pattern)
        log.debug('generated {0} new patterns ending in {1}'.\
                     format(len(cfp),item))
    log.debug('generated {0} patterns'.format(len(patterns)))
    return patterns

def fpGrowthPatterns(ds,k,min_sup=0):
    log.debug('called on ds with {0} elements'.format(len(ds)))
    
    log.debug('building FP-Tree')
    fptree = buildFPTree(ds,min_sup)
    log.debug('FP-Tree built')

    log.debug('running FP-Growth on FP-Tree')
    patterns = mineFPTree(fptree,k,min_sup)
    log.info('FP-Growth found {0} patterns'.format(len(patterns)))

    return patterns

######################################################################
# Eclat
######################################################################
# Eclat stands for Equivalence CLAss Transform.
#
# This algorithm is based around the properties of the vertical data
# format, in which each item has an associated transaction id set
# (tidset).  The support of an individual item is simply the
# cardinality of its tidset.  The support of more than one item is
# simply the cardinality of the intersection of the tidsets of the
# items.
#
# To find all the k-patterns on a dataset, Eclat simply iterates over
# all k-combinations of items and for each it checks the cardinality
# of the intersection of the items in the combination.  If the
# cardinality is at least the minimum support, it reports the pattern.
######################################################################

def eclatPatterns(vds,k,min_sup=0):
    log.debug('called')
    if not hasattr(vds,'__IS_VERTICAL__'):
        ds = vds
        vds = VerticalDataset()
        vds.readFromDataset(ds)

    patterns = []
    combs = combinations(vds.tidsets.keys(),k)
    for tup in combs:
        sets = map(lambda x: vds.tidsets[x],tup)
        items = reduce(lambda x,y: x & y if len(x & y) >= min_sup else set(),\
                           sets)
        if len(items) >= min_sup:
            patterns.append(list(tup))
    log.info('found {0} frequent patterns'.format(len(patterns)))
    return patterns

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

    log.info("Read {0} lines in {1}".format(len(ds),filename))

    patterns = aprioriPatterns(ds,k,len(ds)/2)
    
    print 'found {0} patterns of size {1}'.format(len(patterns),k)
    if max_results == -1:
        max_results = len(patterns)
    for i in range(min(len(patterns),max_results)):
        print patterns[i]

    max_results = -1
    if len(sys.argv) > 3:
        max_results = int(sys.argv[3])
        
    patterns = fpGrowthPatterns(ds,k,len(ds)/2)
    
    print 'found {0} patterns of size {1}'.format(len(patterns),k)
    if max_results == -1:
        max_results = len(patterns)
    for i in range(min(len(patterns),max_results)):
        print patterns[i]
        
    vds = VerticalDataset()
    vds.readFromDataset(ds)
    patterns = eclatPatterns(vds,k,len(ds)/2)
    
    print 'found {0} patterns of size {1}'.format(len(patterns),k)
    if max_results == -1:
        max_results = len(patterns)
    for i in range(min(len(patterns),max_results)):
        print patterns[i]
