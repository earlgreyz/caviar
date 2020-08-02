import unittest

from util.format import OptionalFormat


class FormatTestCase(unittest.TestCase):
    def test_format(self):
        x = OptionalFormat('x')
        self.assertEqual('x', '{}'.format(x))
        x = OptionalFormat(None)
        self.assertEqual('~', '{}'.format(x))
        x = OptionalFormat(.12345)
        self.assertEqual('0.12', '{:.2}'.format(x))


if __name__ == '__main__':
    unittest.main()
