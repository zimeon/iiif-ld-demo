"""Check setup of Python for this tutorial."""

import sys
import unittest


class TestCheckPythonSetup(unittest.TestCase):
    """Check python setup for this tutorial."""

    def test_python_version(self):
        """Need >=2.7 or >=3.3."""
        v = sys.version_info
        if (v[0] == 2):
            self.assertTrue(v >= (2, 7), "Python2 >= 2.7")
        else:
            self.assertTrue(v >= (3, 3), "Python3 >= 3.3")

if __name__ == '__main__':
    unittest.main()
