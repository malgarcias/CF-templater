import sys
import threading
sys.path.append('.')
sys.path.append('..')

import pyCfVpc
import unittest
import random

class getVPCTemplate(unittest.TestCase):
    pass


    def testInvalidCidrBlock(self):
        """'' should raise an exception"""
        self.assertRaises(ValueError, pyCfVpc.validate_cidr,'10.12.0.256/33')

if __name__ == '__main__':
    unittest.main()