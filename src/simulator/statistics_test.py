import unittest
from unittest.mock import Mock

from simulator.statistics import combine, filterLane, AverageResult


class StatisticsTestCase(unittest.TestCase):
    def test_combine(self):
        tt = Mock(return_value=True)
        ff = Mock(return_value=False)
        vehicle = Mock()
        self.assertTrue(combine()(vehicle))
        self.assertTrue(combine(tt)(vehicle))
        self.assertFalse(combine(ff)(vehicle))
        self.assertFalse(combine(tt, ff)(vehicle))
        self.assertFalse(combine(ff, tt)(vehicle))

    def test_filterLane(self):
        vehicle = Mock()
        vehicle.position = 42, 0
        self.assertTrue(filterLane(0)(vehicle))
        self.assertFalse(filterLane(1)(vehicle))
        self.assertFalse(filterLane(2)(vehicle))
        vehicle = Mock()
        vehicle.position = 42, 1
        self.assertTrue(filterLane(1)(vehicle))
        self.assertFalse(filterLane(0)(vehicle))
        self.assertFalse(filterLane(2)(vehicle))


class AverageResultTestCase(unittest.TestCase):
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

    def test_sub(self):
        a = AverageResult(1, 10)
        b = AverageResult(2, 20)
        c = a - b
        self.assertEqual(-1, c.value)
        self.assertEqual(-10, c.count)
        a = AverageResult(10, 20)
        b = AverageResult(1, 2)
        c = a + b
        self.assertEqual(9, c.value)
        self.assertEqual(18, c.count)

    def test_float(self):
        with self.assertRaises(ZeroDivisionError):
            _ = float(AverageResult(42, 0))
        self.assertEqual(.5, float(AverageResult(1, 2)))
        self.assertEqual(.5, float(AverageResult(2, 4)))
        self.assertEqual(2.5, float(AverageResult(5, 2)))

    def test_toMaybeFloat(self):
        self.assertIsNone(float(AverageResult(42, 0)))
        self.assertEqual(.5, float(AverageResult(1, 2)))
        self.assertEqual(.5, float(AverageResult(2, 4)))
        self.assertEqual(2.5, float(AverageResult(5, 2)))


if __name__ == '__main__':
    unittest.main()
