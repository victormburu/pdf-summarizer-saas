#!/usr/bin/env python

import unittest
from rearrange import rearrange_name

class Testrearrange(unittest.TestCase):
    def tets_basic(self):
        testcase = "Lovelace Ada"
        expected = "Ada Lovelace"
        self.assertEqual(rearrange_name(testcase), expected)

    unittest.main()
