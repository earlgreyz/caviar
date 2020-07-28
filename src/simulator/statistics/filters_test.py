import unittest
from unittest.mock import Mock

from simulator.statistics.filters import combine, filterLane


class FiltersTestCase(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
