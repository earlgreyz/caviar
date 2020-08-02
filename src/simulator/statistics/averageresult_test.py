import unittest

from simulator.statistics.averageresult import AverageResult


class MovingMeanTestCase(unittest.TestCase):
    def test_add(self):
        a = AverageResult(1, 10)
        b = AverageResult(2, 20)
        c = a + b
        self.assertEqual(3, c.value)
        self.assertEqual(30, c.count)
        a = AverageResult(0, 0)
        b = AverageResult(1, 2)
        c = a + b
        self.assertEqual(1, c.value)
        self.assertEqual(2, c.count)

    def test_eq(self):
        a = AverageResult(1, 10)
        b = AverageResult(1, 10)
        self.assertTrue(a == b)
        self.assertTrue(b == a)
        self.assertTrue(a == a)
        self.assertTrue(b == b)
        a = AverageResult(10, 10)
        b = AverageResult(20, 20)
        self.assertFalse(a == b)
        self.assertFalse(b == a)
        a = AverageResult(10, 10)
        b = AverageResult(10, 20)
        self.assertFalse(a == b)
        self.assertFalse(b == a)
        a = AverageResult(20, 10)
        b = AverageResult(20, 20)
        self.assertFalse(a == b)
        self.assertFalse(b == a)

    def test_sub(self):
        a = AverageResult(1, 10)
        b = AverageResult(2, 20)
        c = a - b
        self.assertEqual(-1, c.value)
        self.assertEqual(-10, c.count)
        a = AverageResult(10, 20)
        b = AverageResult(1, 2)
        c = a - b
        self.assertEqual(9, c.value)
        self.assertEqual(18, c.count)

    def test_float(self):
        with self.assertRaises(ZeroDivisionError):
            _ = float(AverageResult(42, 0))
        self.assertEqual(.5, float(AverageResult(1, 2)))
        self.assertEqual(.5, float(AverageResult(2, 4)))
        self.assertEqual(2.5, float(AverageResult(5, 2)))

    def test_str(self):
        self.assertEqual('0/0', str(AverageResult(0, 0)))
        self.assertEqual('42/1', str(AverageResult(42, 1)))
        self.assertEqual('1/42', str(AverageResult(1, 42)))

    def test_toMaybeFloat(self):
        self.assertIsNone(AverageResult(42, 0).toMaybeFloat())
        self.assertEqual(.5, AverageResult(1, 2).toMaybeFloat())
        self.assertEqual(.5, AverageResult(2, 4).toMaybeFloat())
        self.assertEqual(2.5, AverageResult(5, 2).toMaybeFloat())

    def test_toZeroFloat(self):
        self.assertEqual(0, AverageResult(42, 0).toZeroFloat())
        self.assertEqual(.5, AverageResult(1, 2).toZeroFloat())
        self.assertEqual(.5, AverageResult(2, 4).toZeroFloat())
        self.assertEqual(2.5, AverageResult(5, 2).toZeroFloat())


if __name__ == '__main__':
    unittest.main()
