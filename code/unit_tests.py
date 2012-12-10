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

class TestFrequentPatternFunctions(unittest.TestCase):

    def test_combinations(self):
        items = [1,2,3,4,5,6,7,8,9]

        for i in range(len(items)-1):
            r = len(items) - i

            icombs = [list(val) for val in itertools.combinations(items,r)]
            fcombs = fp_mining.combsOfSize(items,r)
        
            self.assertEqual(icombs,fcombs)

if __name__ == '__main__':
    unittest.main()
