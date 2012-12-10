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

    def test_combinations(self):
        items = [1,2,3,4,5,6,7,8,9]

        for i in range(len(items)-1):
            r = len(items) - i

            icombs = [list(val) for val in itertools.combinations(items,r)]
            fcombs = fp_mining.combsOfSize(items,r)
        
            self.assertEqual(icombs,fcombs)

class TestDatasetFunctions(unittest.TestCase):

    def test_dataset_conversion(self):
        ds = dataset.Dataset()
        ds.readFromFile('data/tiny.dat')
        vds = dataset.VerticalDataset()
        vds.readFromDataset(ds)
        ds2 = dataset.Dataset()
        ds2.readFromDataset(vds)

        self.assertEqual(ds.rows,ds2.rows)
        
        ds.readFromFile('data/chess_tiny.dat')
        vds = dataset.VerticalDataset()
        vds.readFromDataset(ds)
        ds2 = dataset.Dataset()
        ds2.readFromDataset(vds)

        self.assertEqual(ds.rows,ds2.rows)
        
        ds.readFromFile('data/chess.dat')
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
