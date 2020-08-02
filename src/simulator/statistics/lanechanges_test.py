import unittest

import typing
from unittest.mock import Mock

from simulator.road.road import Road
from simulator.statistics.lanechanges import getLaneChangesFiltered, getLaneChanges
from simulator.vehicle.vehicle import Vehicle


class LaneChangesTestCase(unittest.TestCase):
    def test_getLaneChangesFiltered(self):
        road = Road(100, 2, lane_width=1)
        vehicles: typing.List[Vehicle] = []
        for x in range(10):
            vehicle = Mock()
            vehicle.position = (10 + x, 0)
            vehicle.last_position = (x, 1)
            vehicles.append(vehicle)
        road.getAllVehicles = lambda: vehicles
        # No vehicles matching the predicate.
        result = getLaneChangesFiltered(road, lambda _: False)
        self.assertEqual(0, result)
        # All vehicles matching the predicate.
        result = getLaneChangesFiltered(road, lambda _: True)
        self.assertEqual(10, result)

        # Some vehicles matching the predicate.
        def isEven(vehicle: Vehicle) -> bool:
            x, _ = vehicle.position
            return x % 2 == 0

        result = getLaneChangesFiltered(road, isEven)
        self.assertEqual(5, result)

    def test_getLaneChanges(self):
        road = Road(100, 1, lane_width=1)
        vehicles: typing.List[Vehicle] = []
        for x in range(10):
            vehicle = Mock()
            vehicle.position = (5 + x, 0)
            vehicle.last_position = (x, 1)
            vehicles.append(vehicle)
        for x in range(10, 20):
            vehicle = Mock()
            vehicle.position = (5 + x, 0)
            vehicle.last_position = (x, 0)
            vehicles.append(vehicle)
        road.getAllVehicles = lambda: vehicles
        result = getLaneChanges(road)
        self.assertEqual(10, result)


if __name__ == '__main__':
    unittest.main()
