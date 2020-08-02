import unittest

import typing
from unittest.mock import Mock

from simulator.road.road import Road
from simulator.statistics.decelerations import getDecelerationsFiltered, getDecelerations
from simulator.vehicle.car import Car
from simulator.vehicle.vehicle import Vehicle


class DecelerationsTestCase(unittest.TestCase):
    def test_getDecelerationsFiltered(self):
        road = Road(100, 2, lane_width=1)
        vehicles: typing.List[Vehicle] = []
        for velocity in range(10):
            vehicle = Mock(spec=Car)
            vehicle.velocity = velocity
            vehicle.path = [((0, 0), 12)]
            vehicles.append(vehicle)
        road.getAllActiveVehicles = lambda: vehicles
        # No vehicles matching the predicate.
        result = getDecelerationsFiltered(road, lambda _: False)
        self.assertEqual(0, result)
        # All vehicles matching the predicate.
        result = getDecelerationsFiltered(road, lambda _: True)
        self.assertEqual(10, result)

        # Some vehicles matching the predicate.
        def isEven(vehicle: Vehicle) -> bool:
            return vehicle.velocity % 2 == 0

        result = getDecelerationsFiltered(road, isEven)
        self.assertEqual(5, result)

    def test_getDecelerations(self):
        road = Road(100, 1, lane_width=1)
        vehicles: typing.List[Vehicle] = []
        # Vehicles which decelerated quickly.
        for _ in range(10):
            vehicle = Mock(spec=Car)
            vehicle.velocity = 5
            vehicle.path = [((0, 0), 10)]
            vehicles.append(vehicle)
        # Not cars, therefore should not be counted.
        for _ in range(10):
            vehicle = Mock(spec=Vehicle)
            vehicle.velocity = 5
            vehicle.path = [((0, 0), 10)]
            vehicles.append(vehicle)
        # Vehicles which did not decelerate quickly.
        for _ in range(10):
            vehicle = Mock(spec=Car)
            vehicle.velocity = 9
            vehicle.path = [((0, 0), 10)]
            vehicles.append(vehicle)
        road.getAllActiveVehicles = lambda: vehicles
        result = getDecelerations(road)
        self.assertEqual(10, result)


if __name__ == '__main__':
    unittest.main()
