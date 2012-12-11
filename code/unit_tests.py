#!/usr/bin/env python2.6
######################################################################
# unit_tests.py
######################################################################
# In which we define unit tests for the project.
######################################################################
# For license information, see LICENSE file
# For copyright information, see COPYRIGHT file
######################################################################

import itertools
import unittest
import fp_mining
import dataset

class TestFrequentPatternFunctions(unittest.TestCase):
    """ Unit tests for fp_mining """

class TestDatasetFunctions(unittest.TestCase):

    def test_dataset_conversion(self):
        ds = dataset.Dataset()
        ds.readFromFile('../data/tiny.dat')
        vds = dataset.VerticalDataset()
        vds.readFromDataset(ds)
        ds2 = dataset.Dataset()
        ds2.readFromDataset(vds)

        self.assertEqual(ds.rows,ds2.rows)
        
        ds.readFromFile('../data/chess_tiny.dat')
        vds = dataset.VerticalDataset()
        vds.readFromDataset(ds)
        ds2 = dataset.Dataset()
        ds2.readFromDataset(vds)

        self.assertEqual(ds.rows,ds2.rows)
        
        ds.readFromFile('../data/chess.dat')
        vds = dataset.VerticalDataset()
        vds.readFromDataset(ds)
        ds2 = dataset.Dataset()
        ds2.readFromDataset(vds)

        self.assertEqual(ds.rows,ds2.rows)
            
if __name__ == '__main__':
    tl = unittest.TestLoader()
    suite = tl.loadTestsFromTestCase(TestFrequentPatternFunctions)
    suite.addTest(tl.loadTestsFromTestCase(TestDatasetFunctions))
    unittest.TextTestRunner(verbosity=2).run(suite)
