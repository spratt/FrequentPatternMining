#!/usr/bin/env python2.6
######################################################################
# gp_gv_out.py
######################################################################
# A script that prints the graphviz representation of a FP-Tree.
######################################################################
# For license information, see LICENSE file
# For copyright information, see COPYRIGHT file
######################################################################

import sys
import dataset
from fp_mining import buildFPTree

if len(sys.argv) < 2:
    print "Usage: {0} [file_input]".format(sys.argv[0])
    sys.exit(-1)

ds = dataset.Dataset()
ds.readFromFile(open(sys.argv[1],'rU'))

print buildFPTree(ds,0)
