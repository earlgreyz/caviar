import typing
import unittest
from unittest.mock import Mock

from simulator.road.road import Road
from simulator.statistics.averageresult import AverageResult
from simulator.statistics.velocity import getAverageVelocityFiltered, getAverageVelocity
from simulator.vehicle.vehicle import Vehicle


class VelocityTestCase(unittest.TestCase):
    def test_getAverageVelocityFiltered(self):
        road = Road(100, 1, lane_width=1)
        vehicles: typing.List[Vehicle] = []
        for velocity in range(10):
            vehicle = Mock()
            vehicle.velocity = velocity
            vehicles.append(vehicle)
        road.getAllVehicles = lambda: vehicles
        # No vehicles matching the predicate.
        result = getAverageVelocityFiltered(road, lambda _: False)
        expected = AverageResult(value=0, count=0)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))
        # All vehicles matching the predicate.
        result = getAverageVelocityFiltered(road, lambda _: True)
        expected = AverageResult(value=45, count=10)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

        # Some vehicles matching the predicate.
        def isEven(vehicle):
            return vehicle.velocity % 2 == 0

        result = getAverageVelocityFiltered(road, isEven)
        expected = AverageResult(value=20, count=5)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

    def test_getAverageVelocity(self):
        road = Road(100, 1, lane_width=1)
        vehicles: typing.List[Vehicle] = []
        for velocity in range(10):
            vehicle = Mock()
            vehicle.velocity = velocity
            vehicles.append(vehicle)
        road.getAllVehicles = lambda: vehicles
        result = getAverageVelocity(road)
        expected = AverageResult(value=45, count=10)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))


if __name__ == '__main__':
    unittest.main()
