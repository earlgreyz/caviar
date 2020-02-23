import unittest

from util.rand import shuffled


class TestRandom(unittest.TestCase):
    def test_shuffled(self):
        self.assertListEqual(shuffled([0]), [0])
        sample = list(range(10))
        self.assertEqual(len(shuffled(sample)), len(sample))
        self.assertCountEqual(shuffled(sample), sample)
        sample = [0] * 10
        self.assertEqual(len(shuffled(sample)), len(sample))
        self.assertCountEqual(shuffled(sample), sample)


if __name__ == '__main__':
    unittest.main()
