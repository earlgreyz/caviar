import unittest

from util.dict import makeOrderedDict


class DictTestCase(unittest.TestCase):
    def test_makeOrderedDict(self):
        x = {'a': 1, 'c': 3, 'b': 2}
        y = makeOrderedDict(x, order=['a', 'b', 'c'])
        self.assertListEqual(list(y.keys()), ['a', 'b', 'c'])
        self.assertListEqual(list(y.values()), [1, 2, 3])
        y = makeOrderedDict(x, order=['c', 'b', 'a'])
        self.assertListEqual(list(y.keys()), ['c', 'b', 'a'])
        self.assertListEqual(list(y.values()), [3, 2, 1])


if __name__ == '__main__':
    unittest.main()
