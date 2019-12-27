import sys
import unittest

sys.path.append('.')
sys.path.append('..')

import PyCfVpc


class TestPyCfVPC(unittest.TestCase):
    INVALID_CIDR = '10.12.0.256/33'
    VALID_CIDR = '10.0.0.1/16'
    TEST_STRING = 'Service VPC'
    t = PyCfVpc.PyCfVpc("127.0.0.1/24", "UNITTEST", 443, '0.0.0.0/0', '0.0.0.0/0')

    def test_invalid_CIDR_input(self):
        """'' should raise an exception"""
        self.assertRaises(ValueError, PyCfVpc.validate_cidr, self.INVALID_CIDR)

    def test_valid_CIDR_input(self):
        """'' should assert to True"""
        self.assertTrue(PyCfVpc.validate_cidr(self.VALID_CIDR))

    def test_make_template_not_null(self):
        """'' should assert to Not Null"""
        self.assertIsNotNone(PyCfVpc.make_template(self.t))

    def test_make_template(self):
        """'' should assert the string in the output"""
        self.assertIn(self.TEST_STRING, PyCfVpc.make_template(self.t))


if __name__ == '__main__':
    unittest.main()
