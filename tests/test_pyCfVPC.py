import sys
sys.path.append('.')
sys.path.append('..')

import PyCfVpc
import unittest


class getVPCTemplate(unittest.TestCase):
    
    INVALID_CIDR = '10.12.0.256/33'
    VALID_CIDR = '10.0.0.1/16'
    t = PyCfVpc.PyCfVpc("127.0.0.1/24","UNITTEST",443,'0.0.0.0/0','0.0.0.0/0')

    def testInvalidCIDRInput(self):
        """'' should raise an exception"""
        self.assertRaises(ValueError, PyCfVpc.validate_cidr, self.INVALID_CIDR)

    def testValidCIDRInput(self):
        """'' should assert to True"""
        self.assertTrue(PyCfVpc.validate_cidr(self.VALID_CIDR))

    def test_main_function(self):
        """'' should assert to Not Null"""
        self.assertIsNotNone(PyCfVpc.make_template(self.t))

if __name__ == '__main__':
    unittest.main()