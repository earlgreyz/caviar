import unittest

from simulator.position import inBounds


class TestPosition(unittest.TestCase):
    def test_inBounds(self):
        self.assertTrue(inBounds(2, 1, 5))
        self.assertTrue(inBounds(42, 0, 100))

        self.assertFalse(inBounds(0, 1, 5))
        self.assertFalse(inBounds(10, 20, 100))
        self.assertFalse(inBounds(100, 0, 10))

        self.assertTrue(inBounds(0, 0, 5))
        self.assertTrue(inBounds(10, 10, 100))

        self.assertFalse(inBounds(10, 0, 10))
        self.assertFalse(inBounds(100, 50, 100))


if __name__ == '__main__':
    unittest.main()
