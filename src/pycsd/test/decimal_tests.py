#! /usr/bin/env python
"""
Unittests for the CSD module

"""

import sys

sys.path.append("../csd")
import csd
import unittest

print(dir(csd))

good_values_dict = {32.5: "+0000.+"}


class test__integer_conversion(unittest.TestCase):
    def testToCSD(self) -> None:
        """Check that integers are converted to CSD properly."""

        for key in good_values_dict.keys():
            csd_str = csd.to_csd(key)
            self.assert_(csd_str == good_values_dict[key])


def suite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test__integer_conversion))
    return suite


if __name__ == "__main__":
    unittest.main()
