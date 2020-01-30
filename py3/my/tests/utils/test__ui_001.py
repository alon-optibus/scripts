from __future__ import print_function, division

import unittest

from my.utils.ui_1 import *

########################################################################################################################

TEST_LABEL = 'wow'

########################################################################################################################

class MyTestCase(unittest.TestCase):

    def test__(self):

        self.assertEqual(TEST_LABEL, get_ui_input(label=f'type: {TEST_LABEL} <Enter>'))

        with self.assertRaises(MissingError):
            get_ui_input(label=f'type: {TEST_LABEL} <Esc>')

        self.assertEqual(None, get_ui_input(label=f'type: {TEST_LABEL} <Esc>', default=None))


if __name__ == '__main__':
    unittest.main()

########################################################################################################################
