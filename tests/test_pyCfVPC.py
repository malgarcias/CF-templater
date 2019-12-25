import sys
import threading
sys.path.append('.')
sys.path.append('..')

import pyCfVpc
import unittest
import random

class getVPCTemplate(unittest.TestCase):
    
    INVALID_CIDR = '10.12.0.256/33'
    VALID_CIDR = '10.0.0.1/16'

    def testInvalidCIDRInput(self):
        """'' should raise an exception"""
        self.assertRaises(ValueError, pyCfVpc.validate_cidr,self.INVALID_CIDR)

    def testValidCIDRInput(self):
        """'' should assert to True"""
        self.assertTrue(pyCfVpc.validate_cidr(self.VALID_CIDR))

if __name__ == '__main__':
    unittest.main()